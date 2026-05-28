import ReviewQueuePage from "./pages/ReviewQueuePage";
import LoginPage from "./pages/LoginPage";

function App() {
  const token = localStorage.getItem("token");

  if (!token) {
    return (
      <LoginPage
        onLogin={() => window.location.reload()}
      />
    );
  }

  return <ReviewQueuePage />;
}

export default App;