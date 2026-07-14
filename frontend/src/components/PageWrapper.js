export default function PageWrapper({ children }) {
  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      backgroundColor: "#f4f4f4"
    }}>
      {children}
    </div>
  );
}
