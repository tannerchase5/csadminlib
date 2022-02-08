import smtplib, time

def sendmail(subject:str, toAdd:str, body:str, smtpUser:str, smtpPass:str, log_path:str=None, sleep_time:int=1):
        header = "to: %s\nfrom: %s\nsubject: %s\n" % (toAdd, smtpUser, subject)

        try:
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtpUser, smtpPass)

                server.sendmail(smtpUser, toAdd, header + '\n\n' + body)
                if log_path:
                        with open(log_path, 'a+') as log:
                                log.write("%s\n%s\n\n" % (header, body))
        except Exception as error:
                print(error)
        finally:
                server.quit()
                time.sleep(sleep_time)