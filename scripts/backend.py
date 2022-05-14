import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
from datetime import date
from cryptocmd import CmcScraper
import subprocess
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

class get_crypto_information:
    def __init__(self, crypto_fullname, crypto_shortname):
        self.crypto_fullname = crypto_fullname
        self.crypto_shortname = crypto_shortname
        
    def get_audit(self, crypto_fullname):
        coin_name = crypto_fullname.lower()
        url = "https://leaderboard.certik.io/projects/" + coin_name
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        if str(soup).find("No assessment has been done yet.") != -1 or str(r)=="<Response [404]>":
            yes_no = 0
        else :
            yes_no = 1
        return yes_no # 0 is not audited and 1 is audited
    
    def get_whitepaper(self, crypto_fullname):
        coin_name = crypto_fullname
        coin_name  = coin_name[0].upper() + coin_name[1:]
        url = "https://www.allcryptowhitepapers.com/" + coin_name + "-Whitepaper/"
        r = requests.get(url)
        if str(r)=="<Response [404]>" :
            yes_no = 0
        else :
            soup = BeautifulSoup(r.text, "html.parser")
            paper = soup.find("div", attrs={"class":"entry-content"})
            paper_ = paper.find_all("p")
            yes_no = 0
            for i in range(0, len(paper_)) :
                link = paper_[i].find_all("a")
                for j in range(0, len(link)):
                    if "pdf" in str(link[j]) or "PDF" in str(link[j]) or (coin_name+" Whitepaper" in str(link[j]) and "https://" in str(link[j])):
                        yes_no = 1
                        break
                if yes_no == 1:
                    break
        return yes_no  # 1 is had whitepaper, 0 is not
    
    def get_active_users(self, subreddit):
        subreddit = subreddit
        headers = {
        "User-Agent": "don't rate limit me"
        }
        url = "http://www.reddit.com/r/{}/about.json".format(subreddit)
        resp = requests.get(url, headers=headers)
        if not resp.ok:
            # handle request error, return -1?
            return 0
        content = resp.json()
        try:
            accounts_active = content["data"]["accounts_active"]
        except:
            accounts_active = 0
        return accounts_active
    
    def get_number_github_commit(self, crypto_fullname):
        api_repos = "https://api.github.com/orgs/crypto_name/repos"
        api_commit = "https://api.github.com/repos/crypto_name/repo_name/branches"
        api_sha = "https://api.github.com/repos/crypto_name/repo_name/commits?per_page=10000000&sha=_SHA_"
        input_crypto_name = crypto_fullname.lower()
        api_repos_ = api_repos.replace("crypto_name", input_crypto_name)
        repos = requests.get(api_repos_) 
        if str(repos)=="<Response [404]>" :
            return 0
        commit_numbers = []
        repos_json = repos.json()
        for repo in repos_json :
            try :
                repo_name = repo["name"]
            except :
                return 0
            url = "https://github.com/crypto_name/"+repo_name
            url = url.replace("crypto_name",input_crypto_name)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            commits = soup.find_all("span", attrs={"class":"d-none d-sm-inline"})
            commit_found = None
            commit_number = 0
            for commit in commits:
                commit_found = commit.find("span",attrs={"aria-label":"Commits on master"}) 
                if commit_found != None :
                    commit_number = commit.find("strong")
                    commit_number_ = int(str(commit_number)[8:-9].replace(",",""))
                    commit_numbers.append(commit_number_)
        total_commit = 0
        for number in commit_numbers:
            number = int(str(number))
            total_commit += number
        return total_commit
    
    def get_number_tweet(self, crypto_fullname, timeout_tweets):
        today = date.today()
        end_date = today
        search_term = crypto_fullname
        from_date = '2020-01-01'
        yourCommand = f"snscrape --since {from_date} twitter-search '{search_term} until:{end_date}' > result-tweets_LFW.txt"
        timeoutSeconds = timeout_tweets
        counter = 0
        try:
            subprocess.check_output(yourCommand, shell=True, timeout=timeoutSeconds)
        except: 
            if os.stat("result-tweets_LFW.txt").st_size == 0:
                counter = 0
            else:
                df = pd.read_csv("result-tweets_LFW.txt", names=['link'])
                counter = df.size

        print('Number Of Tweets : '+ str(counter))
        return counter
    
    def get_average_sold_24h(self, crypto_shortname):
        # initialise scraper with time interval
        scraper = CmcScraper(crypto_shortname)

        # get raw data as list of list
        headers, data = scraper.get_data()

        # get data in a json format
        json_data = scraper.get_data("json")

        # get dataframe for the data
        df = scraper.get_dataframe()
        return float(df["Volume"].mean())
    
    def get_marketcap(self, crypto_shortname):
        # initialise scraper with time interval
        scraper = CmcScraper(crypto_shortname)

        # get raw data as list of list
        headers, data = scraper.get_data()

        # get data in a json format
        json_data = scraper.get_data("json")

        # export the data to csv
        scraper.export("csv", name=crypto_shortname+"_all_time")
        return scraper.get_dataframe()
    
    def process_all(self,timeout_tweets = 10):
        # timeout_tweets is timeout to get number of tweets (s)
        crypto_fullname = self.crypto_fullname
        crypto_shortname = self.crypto_shortname
        marketcap = self.get_marketcap(crypto_shortname)
        print("process count avg 24h ... ")
        avg_sold_24h = self.get_average_sold_24h(crypto_shortname)
        print("avg_sold_24h: ", avg_sold_24h)
        print("Processing count github commits ...")
        number_github_commit = self.get_number_github_commit(crypto_fullname)
        print("number_github_commit: ", number_github_commit)
        print("Processing count number of active user in sub reddit ...")
        number_active_reddit = self.get_active_users(crypto_fullname)
        print("number_active_reddit: ", number_active_reddit)
        check_whitepaper = self.get_whitepaper(crypto_fullname) # 1 is had whitepaper, 0 is not
        print("check_whitepaper: ", check_whitepaper)
        check_audit = self.get_audit(crypto_fullname) # 1 is audited and 0 is not audited 
        print("check_audit: ", check_audit)
        print("Processing number of tweet ...")
        number_tweet = self.get_number_tweet(crypto_fullname, timeout_tweets)
        return avg_sold_24h, number_github_commit, number_active_reddit, check_whitepaper, check_audit, number_tweet, marketcap




def main(): 
    model = keras.models.load_model("finalModel.h5")
    aliveCoinData = np.loadtxt('aliveCoinData.txt')
    deadCoinData = np.loadtxt('deadCoinData.txt')
    finData = np.concatenate((deadCoinData, aliveCoinData))
    X = finData[:,0:6]
    y = finData[:,6]
    scaler_X = MinMaxScaler().fit(X)

    import socket
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.bind(('127.0.0.1', 10111))
    socket.listen(10)

    while 1:
        connection, address= socket.accept()
        phpData = connection.recv(1024)
        if phpData:
            decodeData = phpData.decode().split("--")
            if len(decodeData[0]) !=0:
                _fileName = decodeData[0]
                _value1 = decodeData[1]
                _value2 = decodeData[2]

            else:
                _fileName = "None"
                _value1 = "None"
                _value2 = "None"
        try:
            dead_avg_sold_24h = np.zeros((1,1))
            dead_number_github_commit = np.zeros((1,1))
            dead_number_active_reddit = np.zeros((1,1))
            dead_check_whitepaper = np.zeros((1,1))
            dead_check_audit = np.zeros((1,1))
            dead_number_tweet = np.zeros((1,1))
            dead_avg_sold_24h[0],dead_number_github_commit[0],dead_number_active_reddit[0],dead_check_whitepaper[0],dead_check_audit[0],dead_number_tweet[0],_ = get_crypto_information(_value1, _value2).process_all(timeout_tweets=10)
            CoinData = np.zeros((1,6))
            CoinData[:,0] = dead_avg_sold_24h.flatten()
            CoinData[:,1] = dead_number_github_commit.flatten()
            CoinData[:,2] = dead_number_active_reddit.flatten()
            CoinData[:,3] = dead_check_whitepaper.flatten()
            CoinData[:,4] = dead_check_audit.flatten()
            CoinData[:,5] = dead_number_tweet.flatten()

            CoinData = scaler_X.transform(CoinData)
            result = model.predict(CoinData)[0][0] * 100
        except Exception as e:
            result = "Error from code"
        textCorrectRec = str(result)
        print("ok")
        data = f'{textCorrectRec}'.encode()
        connection.sendall(data)
        print(_value1, _value2)
        connection.close()

if __name__ == "__main__":
    main()