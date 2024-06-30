import pandas as pd
import plotly.express as px
import streamlit as st
import mysql.connector
import pymongo
from googleapiclient.discovery import build

#page
st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing ",layout= "wide")


#create menu
with st.sidebar:
    selected =  st.selectbox('my project',("scarping","transform","view"))

#mongodb connection 
from pymongo.mongo_client import MongoClient
client=MongoClient('mongodb://localhost:27017/')
db=client.renu
channel=db.channel

#sql database
mydb= mysql.connector.connect(
    host ='localhost',
    user='root',
    password='3690',
    database = "project"
)
mycursor=mydb.cursor(buffered=True)
mycursor.execute("USE project")



api_key = "AIzaSyC2oQo1iLY7L4n3xPAdamlm9FS3QFphKTQ" 
youtube = build('youtube','v3',developerKey=api_key)


#channel details
def channel_details(channel_id):
    ch_data = []
    response = youtube.channels().list(part = 'snippet,contentDetails,statistics',
                                     id= channel_id).execute()

    for i in range(len(response['items'])):
        data = dict(
                    channel_id=response['items'][i]['id'],
                    channel_name= response ['items'][i]['snippet']['title'],                                    ###channel_name
                    description=response ['items'][i]['snippet']['description'],                               #### description
                    subscribers=response ['items'][i]['statistics']['subscriberCount'],                        #### subscribercount
                    view_count=response ['items'][i]['statistics']['viewCount'],                               #### view count
                    video_count=response ['items'][i]['statistics']['videoCount'],                            #### video count
                    publish_date=response ['items'][i]['snippet']['publishedAt'],                              #### published at
                    play_list=response ['items'][i]['contentDetails']['relatedPlaylists']['uploads']           #### play list
                    )
        ch_data.append(data)
    return ch_data

#video ids 
def get_channel_videos(channel_id):
    ch_data = []
    response = youtube.channels().list(part = 'snippet,contentDetails,statistics',
                                     id= channel_id).execute()

    for i in range(len(response['items'])):
        data = dict(Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        ch_data.append(data)
        d=ch_data[0]['Playlist_id']
    video_id=[]
    request= youtube.playlistItems().list(
                            part="snippet,contentDetails",
                            playlistId=d,
                            maxResults=10)
    response=request.execute()
    for i in range(len(response['items'])):
        data=dict(videoid=response ['items'][i]['contentDetails']['videoId'])
    
        video_id.append(data)


    video_ids = [i['videoid'] for i in video_id]
    return video_ids

#playlist details
def playlists_id(channel_id):
    ch_data = []
    response = youtube.channels().list(part = 'snippet,contentDetails,statistics',
                                     id= channel_id).execute()

    for i in range(len(response['items'])):
        data = dict(Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        ch_data.append(data)
    d=ch_data[0]['Playlist_id']
    print(d)
    play_l=[]
    request= youtube.playlistItems().list(
                            part="snippet,contentDetails",
                            playlistId=d,
                            maxResults=1
                                       )
    response=request.execute()
    for i in range(len(response['items'])):
        data=dict(play_list_id=response ['items'][i]['snippet']['playlistId'],
                  channel_id=response ['items'][i]['snippet']['channelId'],
              play_list_name=response ['items'][i]['snippet']['channelTitle'])
#               videoid=response ['items'][i]['contentDetails']['videoId'])
        # dic.append(data)
        play_l.append(data)
    return play_l

#video_id duration convert to sec
def duration(duration_str):
    if not duration_str.startswith('PT'):
        return "Invalid duration format"
    
    duration_str = duration_str[2:]
    hours,minutes,seconds=0,0,0
    if 'H' in duration_str:
        hours_part,duration_str=duration_str.split('H')
        hours=int(hours_part)
    if 'M' in duration_str:
        minutes_part,duration_str=duration_str.split('M')
        minutes = int(minutes_part)
    if 'S' in duration_str:  
        seconds =int(duration_str.split('S')[0])
    # return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        d=(hours*3600)+(minutes*60)+(seconds)
        return d

#video details
def get_video_details(v_id):
    video_stats=[]
    for j in v_id:
        request= youtube.videos().list(
                                     part="snippet,contentDetails,statistics",
                                     id=j,
                                     maxResults=10
                                      )
        response=request.execute()
        for i in range(len(response['items'])):
            data = dict(video_id              =response ['items'][i]['id'],                       
                  video_name            =response ['items'][i]['snippet']['title'],
                  channel_name            =response ['items'][i]['snippet']['channelTitle'],
                  video_description     =response ['items'][i]['snippet']['description'],            
                  video_view_count      =response ['items'][i]['statistics']['viewCount'],                
                  video_likes           =response ['items'][i]['statistics']['likeCount'],         
                    duration            =duration(response ['items'][i]['contentDetails']['duration']),  
                  video_comment_count   =response ['items'][i]['statistics']['commentCount'],
                  video_favorite_count   =response ['items'][i]['statistics']['favoriteCount'],
                  video_publishedAt     =response ['items'][i]['snippet']['publishedAt'],
                  thumbnails        =response ['items'][i]['snippet']['thumbnails']['default']['url'],
                  channel_id        =response ['items'][i]['snippet']['channelId']
                  )
            video_stats.append(data) 
    return video_stats


#comment details
def channels_comment(v_ids):
    id=[]
    comment_data = []
    for j in v_ids:
        request= youtube.commentThreads().list(
                                     part="snippet,replies",
                                     videoId=j,
                                     maxResults=5
                                        )
        response=request.execute()
        for i in range(len(response['items'])):
            data=dict(
               video_id=response['items'][i]['snippet']['videoId'],
               comment_id=response['items'][i]['snippet']['topLevelComment']['id'],
               comment_text=response ['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'],
               comment_author=response ['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
               comment_publishedAt=response ['items'][i]['snippet']['topLevelComment']['snippet']['updatedAt'],
             )
            id.append(data)
            # new_dic.append(data) 
            # dic.append(data) 
            result = {}
            for comment in id:
                video_id = comment['video_id']
                comment_id = comment['comment_id']
                comment_text = comment['comment_text']
                comment_author = comment['comment_author']
                comment_publishedAt = comment['comment_publishedAt']

                if video_id not in result:
                    result[video_id] = []

                result[video_id].append({
                             'video_id':video_id,
                            'comment_id': comment_id,
                            'comment_text': comment_text,
                            'comment_author': comment_author,
                            'comment_publishedAt': comment_publishedAt
    })
                # result
    comment_data.append(result)

    return comment_data


#get the channel name for mongodb
def channel_names():   
    ch_name = []
    dass=[]
    for i in channel.find({},{"_id":0,'channel_details.channel_name':1}):
        ch_name.append(i)
        # st.write(ch_name)
    for j in ch_name:
            a=j['channel_details'][0]['channel_name']
            dass.append(a)
    return dass

# scarping the data for apl key
if selected == 'scarping':
    id=st.text_input("enter the channel_id:")
    if st.button("scarping"):
            dic=[]
            ch_details = channel_details(id)
            v_ids = get_channel_videos(id)
            play_details=playlists_id(id)
            vid_details = get_video_details(v_ids)
            cmt_details=channels_comment(v_ids)
            data={'channel_details':ch_details,
                "playlist_details":play_details,
                'video_details':vid_details,
                'comment_details':cmt_details}
            
            
            st.write(f'#### scarping data from :green["{ch_details[0]["channel_name"]}"] channel')
            st.write(data)
    if st.button("upload to mongodb"):
                dic=[]
                ch_details = channel_details(id)
                v_ids = get_channel_videos(id)
                play_details=playlists_id(id)
                vid_details = get_video_details(v_ids)
                cmt_details=channels_comment(v_ids)
                data={'channel_details':ch_details,
          "playlist_details":play_details,
                'video_details':vid_details,
                'comment_details':cmt_details}
                dic.append(data)
                
                ids=[]
                for i in channel.find({},{'_id':0,'channel_details.channel_id':1}):
                    ids.append(i)
    # ids
                ids1=[]
                for d in ids:
                    a=d['channel_details'][0]['channel_id']
                    ids1.append(a)
    # ids1
                if id in ids1:
                    st.write('this is is already exis')
                else:
                    channel.insert_many(dic)
                    st.write("Upload to MongoDB successful !!")

#mongo db to sql push the data 
def all_table():
    mydb= mysql.connector.connect(
    host ='localhost',
    user='root',
    password='3690',
    database = "project")
    mycursor=mydb.cursor(buffered=True)
    mycursor.execute("USE project")
    

    query="""SELECT channel_name FROM channel_details"""
    mycursor.execute(query)
    data =mycursor.fetchall()
    channel2=[]
    for i in data:
        channel2.append(i[0])

    if user_inp in channel2:
            st.write ('channel all ready exist')
    else:
        st.write('new channel')
        sql_channel1='''insert into channel_details(
                        channel_id ,
                        channel_name,
                        description ,
                        subscribers,
                        view_count,
                        video_count ,
                        publish_date,
                        play_list)   values (%s,%s,%s,%s,%s,%s,%s,%s)'''
        for i in a:
                value=tuple(i.values())
                mycursor.execute(sql_channel1,value)
                mydb.commit()    
        sql_playlist='''insert into playlist_details(
                        play_list_id ,
                        channel_id,
                        play_list_name)   values (%s,%s,%s)'''
        for i in d:
                value=tuple(i.values())
                mycursor.execute(sql_playlist,value)
                mydb.commit()   
        sql_videos='''insert into video_details(
                        video_id,
                        video_name,
                        channel_name,
                        video_description,
                        video_view_count,
                        video_likes,
                        duration,
                        video_comment_count,
                        video_favorite_count,
                        video_publishedAt,
                        thumbnails,
                        channel_id
                        )   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        for i in b:
                value=tuple(i.values())
                mycursor.execute(sql_videos,value)
                mydb.commit()   
        sql_comments='''insert into comment_details(
                            video_id,
                            comment_id,
                            comment_text,
                            comment_author,
                            comment_publishedAt
                            )   values (%s,%s,%s,%s,%s)'''
        for i in c:
                value=tuple(i.values())
                mycursor.execute(sql_comments,value)
                mydb.commit()   

# user_inp=2
                
if selected =="transform":          
        st.markdown("## Select a channel and Transformation to SQL")
        ch_names = channel_names() 
        # st.write(ch_names)
        user_inp = st.selectbox("Select channel",options= ch_names)     
        for all_de in channel.find({'channel_details.channel_name':user_inp},{'_id':0}):
            # st.write(all_de)
            a=all_de['channel_details']
            st.table(a)
            # channel_df=pd.DataFrame(a)
            d=all_de['playlist_details']
            # playlist_df=pd.DataFrame(d)
            b=all_de['video_details']
            # video_df=pd.DataFrame(b)
            comment_video_id=[]
            for k in range(0,10):
                k=all_de['video_details'][k]['video_id']
                comment_video_id.append(k)
            # print(comment_video_id)    
            g=[]
            for i in comment_video_id:
                g.append(all_de['comment_details'][0][i])
            c= [item for sublist in g for item in sublist]
    # comment_df=pd.DataFrame(c)


            
            if st.button("Submit"):
                all_table()
      
      
#data analysis     
if selected =="view":
    
    st.write("## Select any one question")
    questions = st.selectbox('Questions',
    ['1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])
            

        
        
    if questions == '1. What are the names of all the videos and their corresponding channels?':
        mycursor.execute("""SELECT channel_name , video_name FROM video_details
                            order BY channel_name""")
        out=mycursor.fetchall()
        # print(tabulate(out,headers=[i[0] for i in mycursor.description],  tablefmt='psql'))
        df = pd.DataFrame(out,columns=mycursor.column_names)
        st.write(df)


    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        mycursor.execute("""SELECT channel_name , video_count as total_videos
                            FROM channel_details
                            ORDER BY total_videos DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
    
    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':

        mycursor.execute("""SELECT channel_name , video_view_count as views
                            FROM video_details
                            ORDER BY views DESC
                            limit 10""")

        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
        
    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT video_name , video_comment_count as comment_count
                            FROM video_details
                            ORDER BY video_name""")

        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
        
    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name , video_likes
                                    FROM video_details
                                    ORDER BY video_likes DESC
                                    limit 10""")

        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
        
    elif questions == '6. What is the total number of likes for each video, and what are their corresponding video names?':
        mycursor.execute("""select video_name, video_likes
                         from video_details 
                         order by video_likes  desc""")
        df=pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
    

    elif questions ==  '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        mycursor.execute("""select channel_name , view_count
                                    from channel_details
                                    order by view_count DESC
                                    """)

        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
        
    elif questions =='8. What are the names of all the channels that have published videos in the year 2022?':
        mycursor.execute("""select channel_name 
                            from channel_details
                            where publish_date like '2022%'
                            group by channel_name
                        """)
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)

    
    
    elif questions =='9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name ,
                                    AVG(duration)/60 AS "average_video_duration (sec)"
                                    FROM video_details
                                    GROUP BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
        
    elif questions ==  '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name,video_comment_count as comment_count
                                    FROM video_details
                                    ORDER BY comment_count DESC
                                    limit 1""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        
        st.write(df)