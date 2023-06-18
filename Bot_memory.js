#########
#   👀  #
#########
import java.io.*;
import java.util.*;

public class ChatBot {
    private static final String CHAT_HISTORY_FILE = "your-bot-model_chat_history.txt";

    public static List<String> loadChatHistory() {
        List<String> chatHistory = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(CHAT_HISTORY_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                chatHistory.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return chatHistory;
    }

    public static void saveChatHistory(List<String> chatHistory) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(CHAT_HISTORY_FILE))) {
            for (String line : chatHistory) {
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String callYourBotModel(String prompt) {
        String command = "./your-bot-model/chat " + prompt;
        try {
            Process process = Runtime.getRuntime().exec(command);
            int status = process.waitFor();
            if (status != 0) {
                System.err.println("Error calling your bot model: " + status);
                return "";
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String response = reader.readLine();
            reader.close();
            return response;
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return "";
        }
    }

    public static void main(String[] args) {
        List<String> chatHistory = loadChatHistory();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("You: ");
            String userInput = scanner.nextLine();

            if (userInput.equals("quit")) {
                break;
            }

            chatHistory.add("You: " + userInput);

            StringBuilder promptBuilder = new StringBuilder(" ");
            int startIdx = Math.max(0, chatHistory.size() - 1000);
            for (int i = startIdx; i < chatHistory.size(); i++) {
                promptBuilder.append(chatHistory.get(i)).append(" ");
            }
            String prompt = promptBuilder.toString();

            String aiResponse = callYourBotModel(prompt);
            System.out.println("Your bot model: " + aiResponse);

            chatHistory.add("Your bot model: " + aiResponse);
            saveChatHistory(chatHistory);
        }

        scanner.close();
    }
}
