/#############
/#    👀.    #
/#############

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unistd.h>

using namespace std;

const string CHAT_HISTORY_FILE = "your-bot-model_chat_history.txt";

vector<string> load_chat_history() {
  ifstream f(CHAT_HISTORY_FILE);
  vector<string> chat_history;
  string line;
  while (getline(f, line)) {
    chat_history.push_back(line);
  }
  return chat_history;
}

void save_chat_history(const vector<string>& chat_history) {
  ofstream f(CHAT_HISTORY_FILE);
  for (const string& line : chat_history) {
    f << line << endl;
  }
}

string call_your_bot_model(const string& prompt) {
  string command = "./your-bot-model/chat " + prompt;
  int status = system(command.c_str());
  if (status != 0) {
    cerr << "Error calling your bot model: " << status << endl;
    return "";
  }

  string response;
  ifstream f("/dev/stdout");
  getline(f, response);
  return response;
}

int main() {
  vector<string> chat_history = load_chat_history();

  while (true) {
    cout << "You: ";
    string user_input;
    cin >> user_input;

    if (user_input == "quit") {
      break;
    }

    chat_history.push_back("You: " + user_input);

    string prompt = " ";
    for (int i = chat_history.size() - 1000; i < chat_history.size(); i++) {
      prompt += chat_history[i] + " ";
    }

    string ai_response = call_your_bot_model(prompt);
    cout << "Your bot model: " << ai_response << endl;

    chat_history.push_back("Your bot model: " + ai_response);
    save_chat_history(chat_history);
  }

  return 0;
}
