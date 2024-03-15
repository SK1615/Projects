# KIRANGANESH SURESH (No: 201711361)
cache = []
requests = []

# Function which runs first in first out algorithm
def fifo():
    hits = 0
    for Page in requests:
        if Page in cache:
            print("Hit")
            hits += 1
        else:
            print("Miss")
            if len(cache) < 8:
                cache.append(Page)
            else:
                cache.pop(0)  # Evict the first page
                cache.append(Page)
    print("Final cache list :", cache)
    print("Hits:", hits)

# Function which runs least frequency out algorithm
def lfu():
    global cache
    hits = 0
    Page_Count = {}  # Dictionary to store the frequency of each page
    for Page in requests:
        if Page in cache:
            print("Hit")
            hits += 1
            Page_Count[Page] += 1  # Increment access count
        else:
            print("Miss")
            if len(cache) == 8:
                # Finding out the page with the least frequency
                min_frequency = min(Page_Count.values())
                min_frequency_pages = [page for page, freq in Page_Count.items() if freq == min_frequency]
                eviction_page = min(min_frequency_pages)
                cache.remove(eviction_page)
                del Page_Count[eviction_page]
            cache.append(Page)
            Page_Count[Page] = 1

    print("Final cache List:", cache)
    print("Hits:", hits)
    Page_Count.clear()


# Main program
while True:
    print("Enter the User Page request")
    while True:
        Page = int(input("Enter the page number : ", ))
        if Page == 0:
            break
        requests.append(int(Page))

    print("Choose an algorithm for eviction:")
    print("1. Fifo")
    print("2. LFU")
    print("Q. Quit")
    user_input = input("Press 1 for FIFO, 2 for LFU, or Q to Quit: ")

    if user_input == '1':
        fifo()
    elif user_input == '2':
        lfu()
    elif user_input.upper() == 'Q':
        break
    else:
        print("Program got Terminated, Please try again!")

    # Clear cache and requests for the next run
    cache = []
    requests = []
