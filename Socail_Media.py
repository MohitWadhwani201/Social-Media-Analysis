import os
os.environ['KAGGLE_CONFIG_DIR']='/content'
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('social_media_usage.csv')
df.head()


df=df.dropna()
df=df.drop_duplicates()
# Aggregate data at the App level
app_level_analytics = df.groupby('App').agg({
    'Daily_Minutes_Spent': 'sum',
    'Posts_Per_Day': 'sum',
    'Likes_Per_Day': 'sum',
    'Follows_Per_Day': 'sum'
}).reset_index()

# Add derived metrics
app_level_analytics['Engagement_Per_Post'] = (
        (app_level_analytics['Likes_Per_Day'] + app_level_analytics['Follows_Per_Day'])
        / app_level_analytics['Posts_Per_Day']
)
app_level_analytics['Minutes_Per_Post'] = (
        app_level_analytics['Daily_Minutes_Spent'] / app_level_analytics['Posts_Per_Day']
)

# Display the app-level analytics
print("App-Level Analytics:\n", app_level_analytics)

# Set up a grid for side-by-side plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Total Daily Minutes Spent by App (Bar Chart)
sns.barplot(ax=axes[0, 0], x='App', y='Daily_Minutes_Spent', data=app_level_analytics, hue='App', palette='viridis', dodge=False)
axes[0, 0].set_title('Total Daily Minutes Spent by App')
axes[0, 0].set_xlabel('App')
axes[0, 0].set_ylabel('Daily Minutes Spent')
axes[0, 0].legend([], [], frameon=False)

# Engagement Per Post by App (Bar Chart)
sns.barplot(ax=axes[0, 1], x='App', y='Engagement_Per_Post', data=app_level_analytics, hue='App', palette='coolwarm', dodge=False)
axes[0, 1].set_title('Engagement Per Post by App')
axes[0, 1].set_xlabel('App')
axes[0, 1].set_ylabel('Engagement Per Post')
axes[0, 1].legend([], [], frameon=False)

print()
# Proportion of Likes Per Day (Pie Chart)
axes[1, 0].pie(
    app_level_analytics['Likes_Per_Day'],
    labels=app_level_analytics['App'],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('Set3', len(app_level_analytics))
)
axes[1, 0].set_title('\n Proportion of Likes Per Day by App')

# Proportion of Follows Per Day (Pie Chart)
axes[1, 1].pie(
    app_level_analytics['Follows_Per_Day'],
    labels=app_level_analytics['App'],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('Set2', len(app_level_analytics))
)
axes[1, 1].set_title('\n Proportion of Follows Per Day by App')

# Adjust layout for better visualization
plt.tight_layout()
plt.show()

# Line Charts Side by Side
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Line Chart for Daily Minutes Spent
sns.lineplot(ax=axes[0], x='App', y='Daily_Minutes_Spent', data=app_level_analytics, marker='o', color='blue')
axes[0].set_title('Total Daily Minutes Spent by App')
axes[0].set_xlabel('App')
axes[0].set_ylabel('Daily Minutes Spent')
axes[0].grid()

# Line Chart for Engagement Per Post
sns.lineplot(ax=axes[1], x='App', y='Engagement_Per_Post', data=app_level_analytics, marker='o', color='green')
axes[1].set_title('Engagement Per Post by App')
axes[1].set_xlabel('App')
axes[1].set_ylabel('Engagement Per Post')
axes[1].grid()

# Adjust layout for better visualization
plt.tight_layout()
plt.show()
