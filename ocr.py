from aip import AipOcr

from settings import API_KEY,APP_ID,SECRET_KEY

class OCR(object):
    def __init__(self):
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    @staticmethod
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            content = fp.read()
            fp.close()
            return content

    def getResult(self,filePath):
        '''
        Returns OCR recognition results
        :param filePath: Picture path
        :return: {'code': 0/1 （whether succeed）,'text':str （information）}
        '''
        image = OCR.get_file_content(filePath)

        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"

        res = self.client.basicGeneral(image,options)
        output = {'code': 0,
                  'text': ''}
        # Error condition
        if( 'error_code' in res):
            output['code'] = 0
            if(res['error_code'] == '17'):
                output['text'] = "Daily traffic exceeds quota"
            else:
                output['text'] = 'error code：{}'.format(res['error_code'])
        # normal situation
        else:
            output['code'] = 1
            text = ''
            for elem in res['words_result']:
                text = text + elem['words'] + '\n'
            output['text'] = text
        return output


# if __name__ == '__main__':
#     test = OCR()
#     a = test.getResult('')
#     print(a)