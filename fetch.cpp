// g++ -std=c++14 -Wall -Wextra -Wpedantic -Wconversion -Werror fetch.cpp -o fetch -lpthread
#include <iostream>
using std::cout;
using std::endl;
#include <fstream>
using std::ifstream;
#include <thread>
using std::thread;
#include <mutex>
using std::mutex;
using std::unique_lock;
#include <deque>
using std::deque;
#include <string>
using std::string;
using std::to_string;
#include <unistd.h>

mutex cout_mx;
int count = 0;
const int URLS_PER_THREAD = 3500;
const string PROGRAM_NAME("python3 dl.py ");

void print(const string& msg)
{
	unique_lock<mutex> guard(cout_mx);
	cout << ("#" + to_string(count++) + " " + msg) << endl;
}

void fetch_urls(deque<string> urls, size_t thread_num)
{
	while (!urls.empty()) {
		string url = urls.front();
		urls.pop_front();
		print(url);
		string cmd(PROGRAM_NAME + url + " >> data/" + to_string(thread_num));
		system(cmd.c_str());
	}	
}

void send_urls(deque<thread>& threadpool, deque<string>& urls)
{
	if (urls.empty())
		return;
	threadpool.emplace_back(fetch_urls, urls, threadpool.size());
	urls.clear();
}

int main()
{
	ifstream ifs("urls.txt");
	deque<string> urls;
	string url;
	deque<thread> threadpool;
	while (ifs >> url) {
		urls.push_back(url);
		if (urls.size() >= URLS_PER_THREAD)
			send_urls(threadpool, urls);
	}
	send_urls(threadpool, urls);
	while (!threadpool.empty()) {
		threadpool.front().join();
		threadpool.pop_front();
	}
}