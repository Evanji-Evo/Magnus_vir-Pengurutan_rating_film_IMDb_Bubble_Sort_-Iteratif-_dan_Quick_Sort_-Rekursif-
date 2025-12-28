import csv
import time
import sys

sys.setrecursionlimit(15000)

#Csv to input
def csv_to_movie(file_path):
    MovieData = [] # Local list is better
    with open(file_path, 'r', encoding='utf-8') as movie_File:
        read_movie_csv = csv.reader(movie_File)
        for row in read_movie_csv:
            MovieData.append(row)
    return MovieData

def get_rating(movie_row):
    try:
        return float(movie_row[2])
    except (ValueError, IndexError):
        return -1.0 

#bubble Sort
def bubbleSort(MovieData, n):
    for i in range(n):
        for j in range(0, n - i - 1):
            if get_rating(MovieData[j]) > get_rating(MovieData[j + 1]):
                MovieData[j], MovieData[j + 1] = MovieData[j + 1], MovieData[j]

#if(get_rating(MovieData[i])> get_rating(MovieData[idx])):

#quick Sort
def partition(MovieData, low, high):
    pivot = MovieData[high]
    idx = low - 1

    for i in range(low,high):
        if float(MovieData[i][2]) <= float(pivot[2]):
            idx += 1
            MovieData[idx], MovieData[i] = MovieData[i], MovieData[idx]

    MovieData[idx+1], MovieData[high] = MovieData[high], MovieData[idx+1]
    return idx+1

def quickSort(MovieData, low, high):
    if low < high:
        pi = partition(MovieData, low, high)
        quickSort(MovieData, low, pi-1)
        quickSort(MovieData, pi + 1, high)



def main():
    file_path = 'Top_10000_Movies_IMDb.csv'
    movie_data_for_bubble = csv_to_movie(file_path)
    movie_data_for_quick = csv_to_movie(file_path)
    n = len(movie_data_for_bubble)

    print("--- Running Bubble Sort ---")
    start_time_bubble = time.perf_counter()
    bubbleSort(movie_data_for_bubble, n)
    end_time_bubble = time.perf_counter()
    print(f'Bubble Sort finished in: {end_time_bubble - start_time_bubble:.4f} seconds')

    print("\n--- Running Quick Sort ---")
    start_time_quick = time.perf_counter()
    quickSort(movie_data_for_quick, 1, len(movie_data_for_quick)-1)
    end_time_quick = time.perf_counter()
    print(f'Quick Sort finished in: {end_time_quick - start_time_quick:.4f} seconds')
    
if __name__ == "__main__":
    main()