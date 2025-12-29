import http.server
import socketserver
import json
import csv
import time
import sys
import copy

# Konfigurasi rekursi (PENTING untuk Quick Sort data besar)
sys.setrecursionlimit(20000)

PORT = 8000
CSV_FILE_PATH = 'Top_10000_Movies_IMDb.csv'
GLOBAL_MOVIE_DATA = []

# --- 1. Load Data (Sama seperti logika main.py) ---
def load_data():
    global GLOBAL_MOVIE_DATA
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as movie_File:
            read_movie_csv = csv.reader(movie_File)
            data = list(read_movie_csv)
            # Bersihkan header jika ada
            try:
                float(data[0][2])
            except:
                data = data[1:]
            GLOBAL_MOVIE_DATA = data
            print(f"[INFO] Data berhasil dimuat: {len(GLOBAL_MOVIE_DATA)} baris.")
    except FileNotFoundError:
        print("[ERROR] File CSV tidak ditemukan.")
        GLOBAL_MOVIE_DATA = []

# --- 2. Algoritma Sorting (Logic Asli Anda) ---
def get_rating(movie_row):
    try:
        return float(movie_row[2])
    except (ValueError, IndexError):
        return -1.0 

def bubbleSort(MovieData, n):
    for i in range(n):
        for j in range(0, n - i - 1):
            if get_rating(MovieData[j]) > get_rating(MovieData[j + 1]):
                MovieData[j], MovieData[j + 1] = MovieData[j + 1], MovieData[j]

def partition(MovieData, low, high):
    pivot = MovieData[high]
    idx = low - 1
    for i in range(low,high):
        try:
            val_i = float(MovieData[i][2])
            val_pivot = float(pivot[2])
        except:
            val_i = -1.0
            val_pivot = -1.0
        if val_i <= val_pivot:
            idx += 1
            MovieData[idx], MovieData[i] = MovieData[i], MovieData[idx]
    MovieData[idx+1], MovieData[high] = MovieData[high], MovieData[idx+1]
    return idx+1

def quickSort(MovieData, low, high):
    if low < high:
        pi = partition(MovieData, low, high)
        quickSort(MovieData, low, pi-1)
        quickSort(MovieData, pi + 1, high)

# --- 3. HTTP Request Handler ---
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    # Handle GET Request (Menampilkan HTML)
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Handle POST Request (API untuk Sorting)
    def do_POST(self):
        if self.path == '/run_sort':
            # 1. Baca data JSON yang dikirim frontend
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data_json = json.loads(post_data)
            
            n_size = int(data_json.get('n', 100))
            total_data = len(GLOBAL_MOVIE_DATA)
            if n_size > total_data: n_size = total_data

            # 2. Siapkan data copy agar data asli aman
            data_bubble = copy.deepcopy(GLOBAL_MOVIE_DATA[:n_size])
            data_quick = copy.deepcopy(GLOBAL_MOVIE_DATA[:n_size])

            print(f"[PROCESS] Running Bubble Sort N={n_size}...")
            start_bubble = time.perf_counter()
            bubbleSort(data_bubble, n_size)
            end_bubble = time.perf_counter()
            time_bubble = end_bubble - start_bubble

            print(f"[PROCESS] Running Quick Sort N={n_size}...")
            start_quick = time.perf_counter()
            quickSort(data_quick, 0, len(data_quick)-1)
            end_quick = time.perf_counter()
            time_quick = end_quick - start_quick

            # 3. Kirim respon balik ke frontend
            response = {
                'n': n_size,
                'bubble_time': round(time_bubble, 5),
                'quick_time': round(time_quick, 5)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404)

# --- 4. Main Execution ---
if __name__ == "__main__":
    load_data()
    # Menggunakan ThreadingTCPServer agar UI tidak hang jika ada multiple request (opsional)
    # Tapi untuk tugas simple, TCPServer biasa cukup.
    with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
        print(f"\n--- Server Berjalan ---")
        print(f"Buka browser di: http://localhost:{PORT}")
        print(f"Tekan Ctrl+C untuk berhenti.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dimatikan.")
            httpd.server_close()