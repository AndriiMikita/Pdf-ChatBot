CSS_T = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

BOT_T = '''
<div class="chat-message bot" style="display: flex; align-items: center;">
    <div class="avatar">
        <img src="https://t4.ftcdn.net/jpg/04/46/38/69/360_F_446386956_DiOrdcxDFWKWFuzVUCugstxz0zOGMHnA.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

USER_T = '''
<div class="chat-message user" style="display: flex; align-items: center;">
    <div class="avatar">
        <img src="https://e7.pngegg.com/pngimages/178/595/png-clipart-user-profile-computer-icons-login-user-avatars-monochrome-black.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''