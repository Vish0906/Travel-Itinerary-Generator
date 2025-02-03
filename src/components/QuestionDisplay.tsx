interface QuestionDisplayProps {
  question: string;
  currentIndex: number;
  totalQuestions: number;
}

const QuestionDisplay = ({ question, currentIndex, totalQuestions }: QuestionDisplayProps) => {
  return (
    <div className="text-center">
      <div className="text-sm text-gray-500 mb-2">
        Question {currentIndex} of {totalQuestions}
      </div>
      <div className="text-xl font-medium text-gray-800 mb-6">
        {question}
      </div>
    </div>
  );
};

export default QuestionDisplay;