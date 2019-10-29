from googleapiclient.discovery import build
import pandas as pd
import requests
from bs4 import BeautifulSoup

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q, max_results ,order="relevance", token=None, location=None, location_radius=None):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", # Part signifies the different types of data you want 
    maxResults=max_results,
    location=location,
    locationRadius=location_radius).execute()

    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    tags = []
    commentAuthor = []
    comments = []
    #commentTime = []
    for search_result in search_response.get("items", []):
        
    	if search_result["id"]["kind"] == "youtube#video":

            title.append(search_result['snippet']['title']) 

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
            likeCount.append(response['items'][0]['statistics']['likeCount'])
            dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])
           # commentTime.append(response['items'][0]['statistics']['publishedAt'])
 
            if 'commentCount' in response['items'][0]['statistics'].keys():
                commentCount.append(response['items'][0]['statistics']['commentCount'])
            else:
                commentCount.append([])
            if 'tags' in response['items'][0]['snippet'].keys():
                tags.append(response['items'][0]['snippet']['tags'])
            else:
                tags.append([])
            
            try:
                
                results = youtube.commentThreads().list(
                part="snippet",
                videoId=search_result['id']['videoId'],
                textFormat="plainText").execute()
            
                for item in results["items"]:
                
                    comment = item["snippet"]["topLevelComment"]
                    author = comment["snippet"]["authorDisplayName"]
                    text = comment["snippet"]["textDisplay"]
                    #published=comment["snippet"]["updatedAt"]
                
                    commentAuthor.append(author)
                    #commentTime.append(published)
                    comments.append(text)
            except:
                
                pass
                      
                     
    comment_dict = {'comment_author':commentAuthor, 'comment':comments}#,'View Count':likeCount}  
                
    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount}
    
    return youtube_dict, comment_dict

def captions_Extract(video_id, keyword):
    
    captionContent = []
    captionVideoId = []
    key = []
    
    for vid_id in video_id:
    
        page_link = "https://www.diycaptions.com/php/get-automatic-captions-as-txt.php?id="+vid_id+"&language=en"
        page_response = requests.get(page_link, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        
        try:
            paragraphs = page_content.find_all("div", { "contenteditable" : "true" })[0].text
                
            captionContent.append("".join(paragraphs))
            captionVideoId.append(vid_id)
            key.append(keyword)
               
        except:
            paragraphs="No Caption"
            captionContent.append(paragraphs)
            captionVideoId.append(vid_id)
            key.append(keyword)
            
    caption_cont = {'captionVideoId':captionVideoId, 'captionContent':captionContent, 'Keyword':key}
    return caption_cont


q_search = input("Enter key to search : ")
no_of_videos = input("Enter the no of videos to be taken : ")

youtube_data, comment_data = youtube_search(q_search, no_of_videos)

dfz = pd.DataFrame.from_dict(youtube_data)


dfz.to_csv('videoData.csv')

df=pd.DataFrame.from_dict(comment_data)
df.to_csv('C:\\Users\\NDH00360\\Desktop\\videoCommentData.csv')

videoId_list = dfz['videoId']

caption_cont = captions_Extract(videoId_list,q_search)

dfm = pd.DataFrame.from_dict(caption_cont)
dfm.to_csv('captionContent.csv')

print("Done")
