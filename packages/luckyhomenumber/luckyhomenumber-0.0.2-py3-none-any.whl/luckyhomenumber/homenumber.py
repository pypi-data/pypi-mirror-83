class Homenumber(object):
    def __init__(self,address_txt):
        self.__version__ = '2020.10.29'
        self._address_txt = address_txt
        self.goodnum = {
            1:"บ้านนั้นจักมีความเจริญรุ่งเรืองทำมาหากินคล่องหากเป็นข้าราชการจะได้ เป็นใหญ่เป็นโตเป็นผู้มากด้วยบริวารหรือพูดแบบรวมๆภาษาพระคือเป็นผู้ที่มี บุญบารมีตามผลของการพยากรณ์",
            2:"บ้านจะทำมาหาเลี้ยงชีพไปได้ แต่อาจจะขัดข้องบ้าง มีหนี้สินพอตัว",
            4:"บ้านนั้นเหมาะแก่การเป็นบ้านพ่อค้าแม่ขาย",
            5:"ปานกลางไม่ว่าผู้อาศัยจะอาชีพใดก็ตาม",
            6:"บ้านนี้เหมาะแก่การค้าขายมากกว่าอาชีพอื่น จะอยู่ได้เพราะอาชีพการค้าอย่างเดียวเท่านั้นหากทำราชการอาจไม่ดีเท่าที่ควรนัก",
            9:"ดีมากทำการอันใดจักมีคนมาคอยเสนอตัวรับใช้ใกล้ชิดปรับทุกข์ผูกมิตรเสมอ เป็นมงคลนักแล",
        }
        self.badnum = {
            3:"บ้านนี้จะเกิดการขัดแย้งอยู่ตลอดเวลาภายในบ้าน หรือมีคนป่วยถึงต้องเข้าโรงหมอรอผ่าตัดอยู่บ่อยครั้ง",
            7:"ตกเลขที่บ้านโจร ทำมาหากินเหนื่อยสายตัวแทบขาดแต่ไม่เคยเหลือ ชักหน้าไม่ถึงหลัง ทำอะไรก็หมด",
            8:"เป็นเรื่องราหู หากดวงคนในบ้านดีจะส่งผลดีเลิศ หากดวงคนในบ้านไม่ดีจะทำให้ตกทุกข์หนัก หรือดวงคนในบ้านไม่แข็งจริงก็จะเกิดเหตุไม่คาดคิดเช่นเป็นทุกข์ หักหลัง ผิดหวัง ชู้สาว",
        }

    @property
    def address_txt(self):
        return self._address_txt

    @address_txt.setter
    def address_txt(self, value):
        if value is None:
            raise ValueError(
                'You have to specify your home address e.g. 1314/123'
            )
        self._address_txt = value

    def is_good_address(self):
        # check if the existing home address is good number
        num = self.calc_num()
        if num in self.goodnum.keys():
            result = "good"
            reason = self.goodnum.get(num)
        elif num in self.badnum.keys():
            result = "bad"
            reason = self.badnum.get(num)
        else:
            result = "out of scope"
            reason = "The 0 number has no explanation"
        msg = f'Your address number {self._address_txt} is {result} because {reason}'
        print(msg)

    def calc_num(self):
        txt = self._address_txt
        num = 0
        while len(txt) > 1:
            splited = list(txt)
            num = [self.to_int(i) for i in splited]
            num = sum(num)
            splited = list(str(num))
            txt = ''.join(splited)
        return self.to_int(num)

    def to_int(self, txt):
        try:
            output = int(txt)
        except Exception as e:
            output = 0
        finally:
            return output

if __name__ == "__main__":
    # normal case
    hm = Homenumber('1488/186')
    hm.is_good_address()
    # bad case
    hm = Homenumber('/')
    hm.is_good_address()