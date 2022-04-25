import win32com.client as client

outlook = client.Dispatch("Outlook.Application")
message = outlook.CreateItem(0)
message.Display()
message.To = 'v-NKappaganthula@shutterfly.com'
message.Subject = 'Trail run'
message.Body = 'Trail successful'
message.Save()
message.Send()