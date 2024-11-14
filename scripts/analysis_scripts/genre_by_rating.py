import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def main(data, show_graph=False):

    df = data

    # Function to define the genre based on the 'genre_and_votes' column
    def definir_genre(df):
        def getGenre(genresWithVotes): 
            # Split the genre_and_votes by commas and take the first genre listed
            if not pd.isna(genresWithVotes):
                genreWithVotes = genresWithVotes.split(',')[0]
                genre = genreWithVotes.split(' ')[0]  # Take the first word as the genre
                return genre
            else:
                return "None"

        # Apply the genre extraction function to the DataFrame
        df['genre'] = df['genre_and_votes'].apply(getGenre)
        return df

    # Apply the genre function to categorize the books
    df = definir_genre(df)

    # Ensure that the necessary columns exist in the DataFrame
    if 'average_rating' in df.columns and 'genre' in df.columns:
        
        # Filter the data: keep books with average rating >= 2 and number of pages <= 1500
        df_filtered = df[(df['average_rating'] >= 2) & (df['number_of_pages'] <= 1500)]
        
        # Group the data by genre, calculate the average rating and count the number of books
        genre_stats = df_filtered.groupby('genre').agg(
            average_rating=('average_rating', 'mean'),  # Mean rating per genre
            book_count=('average_rating', 'size')  # Number of books per genre
        ).reset_index()
        
        # Sort the genres by the number of books in descending order, keeping only the top 50
        genre_stats = genre_stats.sort_values(by='book_count', ascending=False).head(50)
        
        # Sort the genres by average rating for plotting purposes
        genre_stats = genre_stats.sort_values(by='average_rating', ascending=True)

        # Create a figure with a specified size
        fig, ax1 = plt.subplots(figsize=(16, 8))

        # Generate a range of colors for the bars using the Viridis colormap
        colors = plt.cm.viridis(np.linspace(0, 1, len(genre_stats)))

        # Create the bar plot for the number of books per genre
        bars = ax1.bar(genre_stats['genre'], genre_stats['book_count'], color=colors, label='Number of books', alpha=0.7)
        
        # Format the x-axis with a 45-degree rotation for readability
        plt.xticks(rotation=45, ha="right", fontsize=10)

        # Create a secondary axis (y-axis) for the average ratings and plot it
        ax2 = ax1.twinx()  
        ax2.plot(genre_stats['genre'], genre_stats['average_rating'], marker='o', linestyle='-', color='b', label='Average rating')
        
        # Add annotations above the bars indicating the number of books
        for bar in bars:
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=10)
        
        # Set the title and axis labels for the chart
        ax1.set_title('Average Rating and Number of Books by Genre (Top 50)', fontsize=16)
        ax1.set_xlabel('Genre', fontsize=14)
        ax1.set_ylabel('Number of books', fontsize=14)
        ax2.set_ylabel('Average rating', fontsize=14)

        # Customize the tick labels for the y-axes
        ax1.tick_params(axis='y', labelcolor='gray', labelsize=12)
        ax2.tick_params(axis='y', labelcolor='blue', labelsize=12)

        # Add grid lines to the primary y-axis (book count)
        ax1.grid(axis='y', linestyle='--', alpha=0.5)

        # Add legends for both the bar and line plots
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        # Automatically adjust the layout to prevent label clipping
        plt.tight_layout()

        # Show the plot
        plt.savefig("./graphs/BarChart_GenreByRating", bbox_inches="tight")
        if show_graph: plt.show()
        plt.clf()

    else:
        # Print an error message if the required columns are not in the DataFrame
        print("The 'average_rating' and 'genre' columns are not present in the file.")

if __name__ == "__main__":

    CSV_FILE = 'data/Cleaned_books.csv'

    data = pd.read_csv(CSV_FILE)
    main(data=data, show_graph=True)
