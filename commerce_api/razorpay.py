import razorpay

client = razorpay.Client(auth=("rzp_test_2vihLVxlM7UemM", "iMd3Zgtm6WVVCco7z0zCUOFb"))

data = {"amount": 100 * 100, "currency": "INR", "receipt": "ahgjhyyuehuyutq"}
client.order.create(data=data)
