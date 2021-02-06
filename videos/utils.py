
def prepareVideoResponsePacket(video,videotopics):
    respVideo={}
    topics=''
    for videotopic in videotopics:
        if topics=='':
            topics=str(videotopic.topic_id)
        else:
            topics=topics+','+str(videotopic.topic_id)
    respVideo={
        'Id': video.video_id,
        'Name':video.name,
        'Description':video.description,
        'Url':video.url,
        'Thumbnail':video.thumbnail,
        'Language':video.lang,
        'UploadDate':video.upload_date,
        'topics':topics}

    return respVideo

