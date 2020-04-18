from flask import Response, make_response
import xmltodict
import time

def messageHandle(data, service, wechat):
    def textHandle(content):
        # return service.tecent_talking(content, data['FromUserName'])
        return service.tecent_translate(content)

    def imageHandle():
        return 'New features is coming soon!'

    def voiceHandle():
        return 'New features is coming soon!'

    def videoHandle():
        return 'New features is coming soon!'

    def shortvideoHandle():
        return 'New features is coming soon!'

    def locationHandle():
        return 'New features is coming soon!'

    def linkHandle():
        return 'New features is coming soon!'

    print(data)
    data = xmltodict.parse(data)['xml']
    wechat.userManger.addNewUser(data['FromUserName'])

    msgType = data['MsgType']
    if msgType == 'text':
        resContent = textHandle(data['Content'])
        print(data['Content'])
        print(resContent)
    elif msgType == 'image':
        resContent = imageHandle()
    elif msgType == 'voice':
        resContent = voiceHandle()
    elif msgType == 'video':
        resContent = videoHandle()
    elif msgType == 'shortvideo':
        resContent = shortvideoHandle()
    elif msgType == 'location':
        resContent = locationHandle()
    elif msgType == 'link':
        resContent = linkHandle()

    res = """<xml>
    <ToUserName><![CDATA[{}]]></ToUserName>
    <FromUserName><![CDATA[{}]]></FromUserName>
    <CreateTime>{}</CreateTime>
    <MsgType><![CDATA[{}]]></MsgType>
    <Content><![CDATA[{}]]></Content>
</xml>""".format(data['FromUserName'], data['ToUserName'], str(int(time.time())), 'text', resContent)

    print(res)
    response = make_response(res)
    response.content_type = 'text/xml'
    return response
