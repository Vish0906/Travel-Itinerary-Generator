import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import WordDisplay from "@/components/WordDisplay";
import QuestionDisplay from "@/components/QuestionDisplay";

const Index = () => {
  const [currentLetterIndex, setCurrentLetterIndex] = useState(0);
  const [guessedLetters, setGuessedLetters] = useState<string[]>([]);
  const [userInput, setUserInput] = useState("");

  // Example word and questions (in real app, you'd have many words and questions)
  const targetWord = "LEARN";
  const questions = [
    "What's the first letter of 'Lion'?",
    "What letter comes after D in the alphabet?",
    "First letter of the word 'Apple'?",
    "What's the first letter of 'Rain'?",
    "What letter comes after M in the alphabet?",
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const correctLetter = targetWord[currentLetterIndex].toLowerCase();
    
    if (userInput.toLowerCase() === correctLetter) {
      const newGuessedLetters = [...guessedLetters];
      newGuessedLetters[currentLetterIndex] = targetWord[currentLetterIndex];
      setGuessedLetters(newGuessedLetters);
      
      if (currentLetterIndex < targetWord.length - 1) {
        setCurrentLetterIndex(prev => prev + 1);
        toast.success("Correct! Next question.");
      } else {
        toast.success("Congratulations! You've completed the word!");
      }
    } else {
      toast.error("Try again!");
    }
    setUserInput("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-blue-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-purple-800">
          Word Discovery Game
        </h1>
        
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <WordDisplay 
            word={targetWord} 
            guessedLetters={guessedLetters}
            currentIndex={currentLetterIndex}
          />
          
          <QuestionDisplay 
            question={questions[currentLetterIndex]}
            currentIndex={currentLetterIndex + 1}
            totalQuestions={targetWord.length}
          />

          <form onSubmit={handleSubmit} className="mt-8">
            <div className="flex gap-4">
              <Input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                maxLength={1}
                className="text-center text-xl"
                placeholder="Type your answer"
                autoFocus
              />
              <Button type="submit" className="bg-purple-600 hover:bg-purple-700">
                Submit
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Index;