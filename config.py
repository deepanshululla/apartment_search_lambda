template_html = """
<html>
<head>
<style> 
  table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
  th, td {{ padding: 5px; }}
</style>
</head>
    <body><p>Hello, There.</p>
    <p>Here is your data:</p>
    <p>This is 1bhk and 2 bhk sorted by price_per_sq_fit,  movein date and then rate,</p>
    {table}
    <p>Regards,</p>
    <p>Deepanshu</p>
    </body>

</html>
"""

APT_REGEX = "Residence (?P<apt_num>[0-9]+) in (?P<building_name>.*) on (?P<address>.*), (?P<unit_type>.*), (?P<area>[0-9]+) square feet, (?P<rent>\$.*), Available (?P<availability>.*)"

BUILDINGS_WITH_WD = {'Embankment House', 'Revetment House', 'Laguna', 'Aquablu', 'Ellipse'}
HEADERS = ['apt_num', 'building_name', 'address', 'unit_type', 'area', 'rent', 'availability', 'price_per_sq_ft', 'has_washer_dryer']

reciepients_list = [
    "priya.makhija24@gmail.com",
    "deepanshu.lulla@gmail.com"]
sender_email = "deepanshu.lulla@gmail.com"
CHARSET = "UTF-8"