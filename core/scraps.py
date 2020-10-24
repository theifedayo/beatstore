

##for installing pydub
sudo add-apt-repository ppa:mc3man/trusty-media  
sudo apt-get install ffmpeg 


import requests
import json

headers = {'Content-type': 'application/json',
          'Authorization' : 'Bearer sk_test_49bbe885dc33ee12e07e887c9cf818e69c0ca690'
            }

data = {'email': 'ades@gmail.com',
        'amount': "10000",
      'bank': {
          'code': "057",
          'account_number': '0000000000'
      },
      'birthday': '1995-12-2'

}
r = requests.post('https://api.paystack.co/charge',
                headers = headers, 
                data= json.dumps(data))

ans = r.text
print(ans[150:225])
print(ans)

web: gunicorn beatstore.wsgi















# curl https://api.paystack.co/charge \
# -H "Authorization: sk_test_5d792a7903444c0e68e85d01b99ab2358ea928b4" \
# -H "Content-Type: application/json" \
# -d '{ email: "customer@email.com", 
#       amount: "10000",
#       metadata: {
#         custom_fields: [
#           {
#             value: "makurdi",
#             display_name: "Donation for",
#             variable_name: "donation_for"
#           }
#         ]
#       },
#       bank: {
#           code: "057",
#           account_number: "0000000000"
#       },
#       birthday: "1995-12-23"
#     }' \
# -X POST