def GetValidMobileNumber():

    try:

        mobile_number = int(input('Enter your mobile number with country code in format (+91-8XXXXXXX09) :'))

        # if len(mobile_number) != 14:

        #     raise Exception("Mobile Number should be 14 characters long")

        # assert mobile_number[:3] in ['+91','+62','+98']

        return mobile_number
    
    except Exception as E:

        print('This is not a valid number !!!', E)

        return GetValidMobileNumber()
    
    # except AssertionError:

    #     print('The Valid Country Codes Are (+91,+62,+98)')

    #     return GetValidMobileNumber()
    
    # except Exception as E:

    #     print('This is not a valid number !!!')

    #     print("Reason is :",E)

    #     return GetValidMobileNumber()
 


mobile_num = GetValidMobileNumber()


print('User entered valid mobile number is',mobile_num)