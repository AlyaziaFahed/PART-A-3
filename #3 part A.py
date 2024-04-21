import heapq
import random
from datetime import datetime, timedelta


# 001: SocialMediaPost class definition
class SocialMediaPost:
    def __init__(self, datetime, post, person, views=0):
        self.datetime = datetime
        self.post = post
        self.person = person
        self.views = views

    def __repr__(self):
        return f"{self.datetime} - {self.post} by {self.person} ({self.views} views)"

# 002: Hash Table for quick access by datetime
posts_by_datetime = {}

def add_post_to_dict(post): #Defines a function to add a post to the dictionary.
    posts_by_datetime[post.datetime] = post #Stores the post in the dictionary with the post's datetime as the key.

def get_post_by_datetime_from_dict(datetime): #Defines a function to retrieve a post from the dictionary using its datetime.
    return posts_by_datetime.get(datetime, None) # Returns the post associated with the given datetime, or None if no such post exists.

# 003: Binary Search Tree for efficient range queries
class Node:
    def __init__(self, post, datetime):
        self.post = post          # Stores the post object
        self.datetime = datetime  # Stores the datetime of the post for comparison act also as a key
        self.left = None          # Pointer to the left child Node
        self.right = None         # Pointer to the right child Node


class SocialMediaManager:
    def __init__(self):
        self.root = None  # Initializes the root of the BST to None

    def add_post_to_bst(self, post):  # function to add a post to the BST.
        # Converts the post's datetime string to a datetime object for comparison.
        post_datetime = datetime.strptime(post.datetime, "%Y-%m-%d %H:%M:%S")
        if self.root is None:
            # Checks if the BST is empty.
            # Sets the root to a new node if the BST is empty.
            self.root = Node(post, post_datetime)
        else:
            # Calls the private _insert method to add the post recursively if the BST is not empty.
            self._insert(self.root, post, post_datetime)

    def _insert(self, node, post, post_datetime):
        # A private method for inserting a post into the BST recursively.
        if post_datetime < node.datetime:
            # Checks if the new post's datetime is earlier than the current node's datetime.
            if node.left is None:
                # Checks if the left child is empty.
                # Inserts the new node as the left child if it was empty.
                node.left = Node(post, post_datetime)
            else:
                # Recursively inserts into the left subtree.
                self._insert(node.left, post, post_datetime)
        else:
            if node.right is None:
                # Checks if the right child is empty.
                # Inserts the new node as the right child if it was empty.
                node.right = Node(post, post_datetime)
            else:
                # Recursively inserts into the right subtree.
                self._insert(node.right, post, post_datetime)

    def _get_range(self, node, start_datetime, end_datetime, posts):
        if node is not None:  # Check if the current node is not empty
            if start_datetime < node.datetime:  # If the start date is before the node's date
                self._get_range(node.left, start_datetime, end_datetime, posts)  # Recursively search in the left subtree
            if start_datetime <= node.datetime <= end_datetime:  # If the node's date is within the range
                posts.append(node.post)  # Add the node's post to the list
            if node.datetime < end_datetime:  # If the node's date is before the end date
                self._get_range(node.right, start_datetime, end_datetime,posts)  # Recursively search in the right subtree
        return posts  # Return the list of posts found within the range

    def get_posts_in_range_from_bst(self, start_datetime, end_datetime):
        # Retrieve posts in the range
        return self._get_range(self.root, start_datetime, end_datetime, [])


#thsi function is added for specificty instead of asking time and seconds just asks for month and year
    def get_posts_in_month_year_range_from_bst(self, start_month_year, end_month_year):
        # Get the posts in the range using the first day of the start month
        start_datetime = start_month_year.replace(day=1)  # Set to the first day of the start month
        # Find the last day of the end month
        next_month = end_month_year.replace(day=28) + timedelta(days=4)  # Move to the next month and then back to get the last day
        last_day_of_month = next_month - timedelta(days=next_month.day)  # Calculate the last day of the end month
        end_datetime = last_day_of_month  # Set as the last day of the end month
        # Call the existing method to get posts in the datetime range
        return self._get_range(self.root, start_datetime, end_datetime,
                               posts=[])  # Retrieve posts within the date range


# 004: Heap for prioritizing posts by views
class PostHeap:
    def __init__(self):
        self.heap = [] # Initializes an empty list to be used as a heap

    def add_post_to_heap(self, post): # Defines a method to add a new post to the heap
        heapq.heappush(self.heap, (-post.views, post)) # Uses the heappush function from the heapq module to add a new element to the heap.
 # The heap is organized by the number of views in descending order, so we negate the view count (-post.views) because Python’s heapq module implements a min-heap by default. By negating the views, the post with the highest views will be at the root of the heap
    def get_most_viewed_post_from_heap(self): # Defines a method to retrieve and remove the post with the highest view count from the heap.
        if self.heap: # Checks if the heap is not empty
            return heapq.heappop(self.heap)[1] #the heappop function from the heapq module to remove and return the smallest element from the heap (which is actually the post with the highest views because of the negation)
        # The [1] accesses the post object, as the heap elements are tuples where the first element is -post.views and the second element is the post object itself.
        return None

# 005: Utility function to generate random posts
def generate_random_posts(num_posts, max_users=100):
    base_datetime = datetime.now() # Current date and time as the base for generating post dates
    persons = [f"User{i}" for i in range(1, max_users + 1)] # List of user names from User1 to UserN
    texts = ["Post about the weather", "Post about sports", "Post about cooking", "Post about traveling", "Post about studying", "Post about eid", "Post about ramadan", "Post about holiday"] # List of predefined post topics
    manager = SocialMediaManager()# Initialize the BST manager for posts
    post_heap = PostHeap() # Initialize the heap for managing posts by views

    for _ in range(num_posts):
        random_datetime = base_datetime - timedelta(days=random.randint(0, 365), hours=random.randint(0, 24), minutes=random.randint(0, 60))# Generate a random past datetime for the post
        random_person = random.choice(persons) # Randomly select a user for the post
        random_text = random.choice(texts) # Randomly select a topic for the post
        random_views = random.randint(0, 100000) # Generate a random view count
        new_post = SocialMediaPost(datetime=random_datetime.strftime("%Y-%m-%d %H:%M:%S"), post=random_text, person=random_person, views=random_views) # Create a new post object
        manager.add_post_to_bst(new_post) # Add the post to the binary search tree
        post_heap.add_post_to_heap(new_post) # Add the post to the heap
        add_post_to_dict(new_post)  # Add the post to the dictionary(hashtbales)

    return manager, post_heap


# 006: Main program execution
def handle_month_year_input(prompt):
    while True:
        month_year_str = input(prompt)  #give user for a datetime input
        try:
            # chnage the input and create a datetime object for the first day of the month
            return datetime.strptime(month_year_str, "%Y-%m") # Return the parsed datetime object
        except ValueError:
            print("Invalid format. Please enter the month and year in YYYY-MM format.") # Error message for invalid input

if __name__ == "__main__":
    num_posts = int(input("How many posts would you like to generate? ")) # Ask user for the number of posts to generate
    manager, post_heap = generate_random_posts(num_posts) # Generate posts and obtain manager and heap objects

    # Sort posts by views and assign unique IDs
    def get_views(post):
        return post.views

    sorted_posts = sorted(posts_by_datetime.values(), key=get_views, reverse=True) # Sort posts by views in descending order
    posts_with_ids = {f"{i:03}": post for i, post in enumerate(sorted_posts, 1)} # Assign unique IDs to sorted posts

    print("\nGenerated Posts - sorted by views:")  #  header for sorted posts
    for post_id, post in posts_with_ids.items():  # Loop through posts and print them with IDs
        print(f"{post_id}: {post}")

    while True:  # Start an infinite loop for user actions
        print("\nSelect an action:") # Display the menu of actions
        print("1 - Get a post by date")
        print("2 - Display the most viewed post")
        print("3 - Get posts in a specific time range")
        print("4 - Display all posts")
        print("5 - Exit")

        action = input("Enter your choice (1-5): ")  # Get user input for action choice
        if action == "1":  #If user selects to get a post by date
            date_str = input("Enter the date and time (YYYY-MM-DD HH:MM:SS): ")
            post = get_post_by_datetime_from_dict(date_str)  # Retrieve the post for the given date
            print("Post:", post) # Display the retrieved post
        elif action == "2":  # If user wants to see the most viewed post
            most_viewed = post_heap.get_most_viewed_post_from_heap() # Get the most viewed post from the heap
            if most_viewed:
                print("Most viewed post:", most_viewed) # Display the most viewed post
            else:
                print("No posts available.") #else print this
        elif action == "3": # If user selects to get posts in a time range
            start_month_year = handle_month_year_input("Enter the start month and year (YYYY-MM): ") # Get start month/year
            end_month_year = handle_month_year_input("Enter the end month and year (YYYY-MM): ") # Get end month/year
                # Check if the start date is earlier than the end date
            if start_month_year < end_month_year:
                    # Proceed with the BST query
                posts_in_range = manager.get_posts_in_month_year_range_from_bst(start_month_year, end_month_year) # Retrieve posts in range
                for post in posts_in_range: # Loop through the posts in range and display them
                    print(post)
            else:
                    # Display the message only if the start date is not earlier than the end date
                print("The start date must be earlier than the end date. Please try again.")
        elif action == "4": #is they want to display again all posys
            # option to display all posts
            for post_id, post in posts_by_datetime.items(): #loop from items
                print(f"{post_id}: {post}") #print
        elif action == "5": # If user chooses to exit
            print("Thank you for using the post management system. Goodbye!") # Goodbye message
            break # Break the loop to exit
        else:
            print("Invalid action, try again.") # Message for invalid action input


