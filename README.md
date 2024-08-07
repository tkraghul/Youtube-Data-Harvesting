# YouTube Data Explorer: Harvesting & Warehousing YouTube Data and Build an Application Using Streamlit. 
## Project Overview

This project develops a user-friendly Streamlit application, StreamTube Data Explorer, that enables users to access, analyze, and manage data from multiple YouTube channels. By leveraging the YouTube API, the application retrieves detailed channel and video data, stores it in a SQL database, and provides users with the ability to search, query, and visualize the information.
## Features

   *** YouTube Data Retrieval: Input a YouTube channel ID to retrieve channel details, including the channel name, subscriber count, video count,            playlist ID, video IDs, likes, dislikes, comments, and more using the Google API.
   ***Multi-Channel Data Collection: Collect data for up to 10 different YouTube channels and store it in a data lake with a single click.
    SQL Data Warehousing: Option to store the retrieved data in either MySQL or PostgreSQL.
    Advanced Search & Queries: Perform complex searches and retrieve data from the SQL database, including joining tables to get detailed channel         information.
    Data Visualization: Display retrieved data in the Streamlit app using tables, charts, and graphs for easy analysis.

How It Works

    Set Up the Streamlit App: A simple UI allows users to enter a YouTube channel ID, view channel details, and select channels for data migration.
    Connect to the YouTube API: Retrieve channel and video data using the Google API client library for Python.
    Store & Clean Data: Use pandas DataFrames for temporary data storage and cleaning before migrating to the SQL database.
    Migrate Data to SQL: Store the collected data in a MySQL or PostgreSQL database.
    Query the SQL Database: Use SQLAlchemy to perform queries and retrieve specific channel and video details.
    Display Data in Streamlit: Visualize the data within the Streamlit app, providing insights through various charts and tables.

Example SQL Queries

    Names of all videos and their corresponding channels
    Channels with the most videos and the video count
    Top 10 most viewed videos and their respective channels
    Number of comments on each video and corresponding video names
    Videos with the highest number of likes and corresponding channel names
    Total number of likes and dislikes for each video and corresponding video names
    Total number of views for each channel and corresponding channel names
    Channels that published videos in the year 2022
    Average video duration for each channel and corresponding channel names
    Videos with the highest number of comments and corresponding channel names

Results

The project successfully demonstrates the integration of YouTube data harvesting with SQL data warehousing, providing an effective tool for users to analyze YouTube channel data.
Technologies Used

    Python
    Streamlit
    Google API
    SQL (MySQL/PostgreSQL)
    SQLAlchemy
    Pandas

Setup and Installation

    Clone the repository.
    Install the required Python libraries.
    Set up the Google API credentials.
    Configure the SQL database (MySQL or PostgreSQL).
    Run the Streamlit application.

Conclusion

StreamTube Data Explorer showcases the potential of combining API integration, data warehousing, and interactive data visualization using modern tools like Streamlit and SQL databases. It serves as a valuable tool for analyzing social media data, specifically YouTube channels.
