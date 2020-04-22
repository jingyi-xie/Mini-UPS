import yagmail

receiver = "hf65@duke.edu"
body = "Hello there from Yagmail"

yag = yagmail.SMTP("ece568ups@gmail.com")
yag.send(
    to=receiver,
    subject="Yagmail test with attachment",
    contents=body,
)
