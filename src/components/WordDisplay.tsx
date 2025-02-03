import { cn } from "@/lib/utils";

interface WordDisplayProps {
  word: string;
  guessedLetters: string[];
  currentIndex: number;
}

const WordDisplay = ({ word, guessedLetters, currentIndex }: WordDisplayProps) => {
  return (
    <div className="flex justify-center gap-4 mb-8">
      {word.split("").map((letter, index) => (
        <div
          key={index}
          className={cn(
            "w-14 h-14 border-2 flex items-center justify-center text-2xl font-bold rounded-lg transition-all duration-300",
            index === currentIndex
              ? "border-purple-500 bg-purple-50"
              : "border-gray-300",
            guessedLetters[index]
              ? "text-purple-700"
              : "text-transparent"
          )}
        >
          {guessedLetters[index] || letter}
        </div>
      ))}
    </div>
  );
};

export default WordDisplay;