from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('55396448374D66466D697A54375042597934684877586A6D2B3977335173775345566C4F3249497133724D3D')
        params = {
            'sender': '',  # optional
            'receptor': phone_number,  # multiple mobile number, split by comma
            'message': f' کد تایید شما {code} ',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
