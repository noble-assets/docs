import React from "react";

const GitHubButton = ({ repoUrl }) => {
  return (
    <a
      href={repoUrl}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "8px",
        padding: "8px 12px",
        borderRadius: "8px",
        backgroundColor: "#24292e",
        color: "#ffffff",
        textDecoration: "none",
        fontWeight: "bold",
        fontSize: "14px",
        marginBottom: "20px",
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="white"
      >
        <path d="M12 .297C5.373.297 0 5.67 0 12.297c0 5.3 3.438 9.8 8.207 11.387.6.113.793-.26.793-.577v-2.173c-3.338.723-4.043-1.61-4.043-1.61-.546-1.386-1.334-1.756-1.334-1.756-1.09-.746.083-.73.083-.73 1.205.084 1.84 1.24 1.84 1.24 1.07 1.834 2.805 1.304 3.492.997.107-.776.42-1.304.762-1.604-2.665-.303-5.466-1.334-5.466-5.93 0-1.312.47-2.385 1.24-3.227-.124-.303-.537-1.523.118-3.176 0 0 1.008-.322 3.3 1.233a11.482 11.482 0 0 1 3.003-.404c1.018.006 2.043.136 3.003.404 2.292-1.555 3.3-1.233 3.3-1.233.655 1.653.242 2.873.118 3.176.77.842 1.24 1.915 1.24 3.227 0 4.609-2.805 5.624-5.478 5.921.43.37.812 1.102.812 2.22v3.293c0 .32.19.694.8.577C20.565 22.09 24 17.594 24 12.297 24 5.67 18.627.297 12 .297z" />
      </svg>
      GitHub
    </a>
  );
};

export default GitHubButton;
