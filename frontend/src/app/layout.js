import Navbar from "./components/Navbar";

export const metadata = {
  title: "Real-Time Resource Monitor",
  description: "Monitor and manage workers in real-time",
};

export default function RootLayout({ children }) {
  const layoutStyles = {
    height: "100vh",
    width: "100vw",
    backgroundColor: "#2b2b2b",
    color: "#a9b7c6",
    fontFamily: "'JetBrains Mono', monospace",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    overflow: "hidden",
    margin: 0,
    padding: 0,
  };

  const mainStyles = {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "100%",
    height: "100%",
  };

  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body style={layoutStyles}>
        <Navbar />
        <main style={mainStyles}>{children}</main>
      </body>
    </html>
  );
}
