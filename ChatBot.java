import java.io.*;
import java.util.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;

public class ChatBot {
    private static String CHAT_HISTORY_FILE = "chat_history.txt";
    private static String BOT_MODEL_CMD = "./your-bot-model/chat";

    public static List<String> loadChatHistory() {
        if (!Files.exists(Paths.get(CHAT_HISTORY_FILE))) {
            return new ArrayList<>();
        }
        try {
            return Files.readAllLines(Paths.get(CHAT_HISTORY_FILE), StandardCharsets.UTF_8);
        } catch (IOException e) {
            System.err.println("Error loading history: " + e.getMessage());
            return new ArrayList<>();
        }
    }

    public static void saveChatHistory(List<String> chatHistory) {
        try {
            Files.write(Paths.get(CHAT_HISTORY_FILE), chatHistory, StandardCharsets.UTF_8);
        } catch (IOException e) {
            System.err.println("Error saving history: " + e.getMessage());
        }
    }

    public static String callBotModel(String prompt) {
        try {
            // Split command by space to get executable and initial args.
            // This is a simple implementation and might not handle quoted arguments in the command string correctly.
            List<String> command = new ArrayList<>();
            String[] parts = BOT_MODEL_CMD.trim().split("\\s+");
            Collections.addAll(command, parts);

            command.add(prompt);

            ProcessBuilder pb = new ProcessBuilder(command);
            pb.redirectErrorStream(true); // Merge stderr into stdout

            Process process = pb.start();

            StringBuilder output = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append(System.lineSeparator());
                }
            }

            int exitCode = process.waitFor();
            if (exitCode != 0) {
                // If the process failed but produced output (which we captured), we still return it,
                // but usually stderr is more useful here. Since we merged streams, output contains error too.
            }

            return output.toString().trim();

        } catch (IOException | InterruptedException e) {
            System.err.println("Error calling bot model: " + e.getMessage());
            return "";
        }
    }

    public static void main(String[] args) {
        if (args.length > 0) {
            BOT_MODEL_CMD = args[0];
        }
        if (args.length > 1) {
            CHAT_HISTORY_FILE = args[1];
        }

        System.out.println("Using model command: " + BOT_MODEL_CMD);
        System.out.println("Using history file: " + CHAT_HISTORY_FILE);

        List<String> chatHistory = loadChatHistory();
        System.out.println("Loaded " + chatHistory.size() + " lines of history.");
        System.out.println("Type 'quit' or 'exit' to end the session.");

        try (Scanner scanner = new Scanner(System.in)) {
            while (true) {
                System.out.print("You: ");
                if (!scanner.hasNextLine()) break;

                String userInput = scanner.nextLine();

                if (userInput.equalsIgnoreCase("quit") || userInput.equalsIgnoreCase("exit")) {
                    break;
                }

                if (userInput.trim().isEmpty()) continue;

                chatHistory.add("You: " + userInput);

                StringBuilder promptBuilder = new StringBuilder();
                int startIdx = Math.max(0, chatHistory.size() - 1000);
                for (int i = startIdx; i < chatHistory.size(); i++) {
                    promptBuilder.append(chatHistory.get(i)).append("\n");
                }
                String prompt = promptBuilder.toString();

                String aiResponse = callBotModel(prompt);

                if (!aiResponse.isEmpty()) {
                    System.out.println("Bot: " + aiResponse);
                    chatHistory.add("Bot: " + aiResponse);
                    saveChatHistory(chatHistory);
                } else {
                    System.out.println("Bot: [No response]");
                }
            }
        }
    }
}
