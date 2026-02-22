#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdio>
#include <memory>
#include <array>
#include <algorithm>

using namespace std;

// Default configuration
string CHAT_HISTORY_FILE = "chat_history.txt";
string BOT_MODEL_CMD = "./your-bot-model/chat";

// Helper to check file existence
bool file_exists(const string& name) {
    ifstream f(name.c_str());
    return f.good();
}

vector<string> load_chat_history() {
    vector<string> chat_history;
    if (!file_exists(CHAT_HISTORY_FILE)) {
        return chat_history;
    }
    ifstream f(CHAT_HISTORY_FILE);
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

string call_bot_model(const string& prompt) {
    // Construct command. Note: simple string concatenation is vulnerable to injection if prompt has shell metacharacters.
    // Ideally we should use exec/fork, but popen is easier for this level of cleanup.
    // For safety, we should escape the prompt, but for now we assume simple usage.
    // We will wrap the prompt in quotes.

    // Simple escaping for single quotes
    string escaped_prompt = prompt;
    size_t pos = 0;
    while ((pos = escaped_prompt.find("'", pos)) != string::npos) {
        escaped_prompt.replace(pos, 1, "'\\''");
        pos += 4;
    }

    string command = BOT_MODEL_CMD + " '" + escaped_prompt + "'";

    array<char, 128> buffer;
    string result;

    // Open pipe to read output
    unique_ptr<FILE, decltype(&pclose)> pipe(popen(command.c_str(), "r"), pclose);
    if (!pipe) {
        cerr << "popen() failed!" << endl;
        return "";
    }

    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }

    // Remove trailing newline
    if (!result.empty() && result.back() == '\n') {
        result.pop_back();
    }

    return result;
}

int main(int argc, char* argv[]) {
    // Simple argument parsing
    if (argc > 1) {
        BOT_MODEL_CMD = argv[1];
    }
    if (argc > 2) {
        CHAT_HISTORY_FILE = argv[2];
    }

    cout << "Using model command: " << BOT_MODEL_CMD << endl;
    cout << "Using history file: " << CHAT_HISTORY_FILE << endl;

    vector<string> chat_history = load_chat_history();
    cout << "Loaded " << chat_history.size() << " lines of history." << endl;
    cout << "Type 'quit' or 'exit' to end the session." << endl;

    while (true) {
        cout << "You: ";
        string user_input;
        if (!getline(cin, user_input)) {
            break; // EOF
        }

        if (user_input == "quit" || user_input == "exit") {
            break;
        }

        if (user_input.empty()) continue;

        chat_history.push_back("You: " + user_input);

        string prompt = "";
        // Safely calculate start index
        int start_index = max(0, (int)chat_history.size() - 1000);
        for (size_t i = start_index; i < chat_history.size(); i++) {
            prompt += chat_history[i] + "\n";
        }

        string ai_response = call_bot_model(prompt);

        if (!ai_response.empty()) {
            cout << "Bot: " << ai_response << endl;
            chat_history.push_back("Bot: " + ai_response);
            save_chat_history(chat_history);
        } else {
             cout << "Bot: [No response]" << endl;
        }
    }

    return 0;
}
