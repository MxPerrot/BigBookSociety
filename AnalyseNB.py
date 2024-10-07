import pandas as pd
import matplotlib.pyplot as plt

file_path = '/mnt/data/Cleaned_books.csv'
df = pd.read_csv(file_path)

df['date_published'] = pd.to_datetime(df['date_published'], errors='coerce')

df['year_published'] = df['date_published'].dt.year

plt.figure(figsize=(10, 6))
plt.scatter(df['year_published'], df['average_rating'], alpha=0.5, color='blue')

plt.title('Nuage de points: Année de publication vs Note moyenne')
plt.xlabel('Année de publication')
plt.ylabel('Note moyenne')

plt.show()
