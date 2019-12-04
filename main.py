
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd

chromedriver_path = '/Users/kanhaiagarwal/Desktop/chromedriver'
webdriver = webdriver.Chrome(executable_path=chromedriver_path)
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys('fosho.tv')
password = webdriver.find_element_by_name('password')
password.send_keys('Kraiz_23012019')

button_login = webdriver.find_element_by_xpath('(//form//button)[2]')
sleep(1)
button_login.click()
sleep(3)

hashtag_list = ['bakchodindia']

# - if it's the first time you run it, use this line and comment the two below
prev_user_list = []
# prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv',
#                              delimiter=',').iloc[:, 1:2]  # useful to build a user log
# prev_user_list = list(prev_user_list['0'])

new_followed = []
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    print "hashtag: " + hashtag
    webdriver.get('https://www.instagram.com/explore/tags/' +
                  hashtag + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

    first_thumbnail.click()
    sleep(randint(1, 2))
    try:
        x = 1
        while x <= 100:
            username = webdriver.find_element_by_xpath(
                '//div[@class="PdwC2 _6oveC Z_y-9"]//a[@class="FPmhX notranslate nJAzx"]').text
            print "Username: " + username

            if username not in prev_user_list:
                print "Username " + username + " not in the prev_user_list"
                # If we already follow, do not unfollow
                if webdriver.find_element_by_xpath('//div[@class="PdwC2 _6oveC Z_y-9"]//div[@class="bY2yH"]//button').text == 'Follow':
                    print "Follow button found for the username: " + username

                    webdriver.find_element_by_xpath(
                        '//div[@class="PdwC2 _6oveC Z_y-9"]//div[@class="bY2yH"]//button').click()

                    new_followed.append(username)
                    followed += 1
                    sleep(randint(5, 10))
                    # Liking the picture
                    button_like = webdriver.find_element_by_xpath(
                        '//div[@class="PdwC2 _6oveC Z_y-9"]//button[@class="dCJp8 afkep"]/span[@class="glyphsSpriteHeart__outline__24__grey_9 u-__7"]')

                    button_like.click()
                    likes += 1
                    sleep(randint(18, 25))

                    # Comments and tracker
                    comm_prob = randint(1, 10)
                    print('{}_{}: {}'.format(hashtag, x, comm_prob))
                    comments += 1
                    webdriver.find_element_by_xpath(
                        '//div[@class="PdwC2 _6oveC Z_y-9"]//span[@class="_15y0l"]//button').click()
                    comment_box = webdriver.find_element_by_xpath(
                        '//section//form[@class="X7cDz"]//textarea')

                    if (comm_prob <= 5):
                        comment_box.send_keys('Nice Picture :)')
                        sleep(1)
                    else:
                        comment_box.send_keys('So cool! :D')
                        sleep(1)
                    # Enter to post comment
                    comment_box.send_keys(Keys.ENTER)
                    sleep(randint(22, 28))
                    x = x + 1
                else:
                    print "Already following username: " + username

                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(25, 29))
            else:
                print "Username " + username + " present in the prev_user_list"
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(20, 26))
    # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
    except:
        continue

for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv(
    '{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
