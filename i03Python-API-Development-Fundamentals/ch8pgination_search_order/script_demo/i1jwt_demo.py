import base64


header = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
b64 = base64.b64decode(header)
print(b64)

payload = 'eyJpYXQiOjE1NjQ5ODI5OTcsIm5iZiI6MTU2NDk4Mjk5NywianRpI \
joiMGIzOTVlODQtNjFjMy00NjM3LTkwMzYtZjgyZDgyYTllNzc5IiwiZXhwIjoxNTY0 \
OTgzODk3LCJpZGVudGl0eSI6MywiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0'
b64p = base64.b64decode(payload + '==')
print(b64p)
