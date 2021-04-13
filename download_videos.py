import requests
import os
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from os.path import expanduser
from os import sys


def get_args():
    parser = argparse.ArgumentParser(
        description='Download videos from canvas pages')

    # Add the arguments
    parser.add_argument('InputPath',
                        metavar='input_file_path',
                        type=str,
                        help='the path to the input file')

    parser.add_argument('OutputPath',
                        metavar='output_directory_path',
                        type=str,
                        help='the path to the output directory')

    parser.add_argument('Username',
                        metavar='canvas_username',
                        type=str,
                        help='your canvas username')

    parser.add_argument('Password',
                        metavar='canvas_password',
                        type=str,
                        help='your canvas password')

    return parser.parse_args()


def download_videos_from_page(url, output_path):
    # find all video thumbnails
    thumbnails = driver.find_elements_by_class_name(
        'media_comment_thumbnail_play_button')

    # for each thumbnail download the video
    for index, thumbnail in enumerate(thumbnails):
        video_src = get_video_src(thumbnail, index)
        download_video(video_src, output_path)
        close_thumbnail()

# minimize the open video
def close_thumbnail():
    minimize_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Minimize')]")))
    minimize_button.click()


def download_video(video_src, output_path):
    # create output path if not exist
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
        print("Directory '% s' created" % output_path)

    # get file
    r = requests.get(video_src, allow_redirects=True)

    # remove invalid filename chars
    sanitized_title = "".join(x for x in driver.title if x.isalnum())

    filename = sanitized_title + '.mp4'
    full_path = os.path.join(output_path, filename)
    # if this is the second video on the page, rename it
    if (os.path.exists(full_path)):
        filename = sanitized_title + '2.mp4'
        full_path = os.path.join(output_path, filename)

    # write to path
    open(full_path, 'wb').write(r.content)

    print('Downloaded %s' % full_path)


def get_video_src(thumbnail, index):
    # make video start playing
    thumbnail.click()

    # hover over video
    video = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'mep_' + str(index))))
    actions = ActionChains(driver)
    actions.move_to_element(video)

    # hover on sunburst
    sunburst = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="mep_' + str(index) + '"]/div/div[3]/div[7]')))
    actions.move_to_element(sunburst)

    # get option
    options_menu = driver.find_element_by_xpath(
        '//*[@id="mep_' + str(index) + '"]/div/div[3]/div[7]/div')
    quality_choices = options_menu.find_elements_by_xpath("./ul/*")

    # pick the second best quality choice
    if (len(quality_choices) == 1):
        desired_choice = quality_choices[0]
    else:
        desired_choice = quality_choices[-2]

    # move to option and click it
    actions.move_to_element(desired_choice)
    actions.click()

    actions.perform()

    # get url to download
    current_vid = driver.find_element_by_xpath('//video')
    url = current_vid.get_attribute("src")

    return url


def login_to_canvas(username, password):
    # enter username
    username_box = driver.find_element_by_xpath('//*[@id="username"]')
    username_box.send_keys(username)

    # enter password
    password_box = driver.find_element_by_xpath('//*[@id="password"]')
    password_box.send_keys(password)

    # click sign on
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[1]/div/div/form/div[3]/button').click()

# return list of canvas urls from input file
def read_input_file(path):
    if not os.path.exists(path):
        print('The input file specified does not exist')
        sys.exit()
    # read and remove any whitespace
    with open(path) as f:
        urls = f.readlines()
        urls = [line.strip() for line in urls]
        return urls


def start():
    args = get_args()

    global driver
    driver = webdriver.Chrome()
    urls = read_input_file(args.InputPath)

    needs_login = True

    for url in urls:
        try:
            driver.get(url)
            if (needs_login):
                login_to_canvas(args.Username, args.Password)
                needs_login = False
            download_videos_from_page(url, args.OutputPath)
        except Exception as e:
            print('Error downloading video from %s' % url)
            print(e)
            driver.quit()
            driver = webdriver.Chrome()
            needs_login = True


if __name__ == "__main__":
    start()
