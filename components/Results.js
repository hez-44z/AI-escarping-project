import React from "react";


const Results = ({ results }) => {
    const placeholderImage = "https://placehold.co/600x400/EEE/31343C";


    return (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: "20px" }}>
            {results.map((item, index) => (
                <div key={index} style={{ border: "1px solid #ddd", borderRadius: "8px", padding: "10px", textAlign: "center" }}>
                    <img
                        src={item.image_url || placeholderImage}
                        alt={item.title || "Item"}
                        style={{ width: "100%", height: "150px", objectFit: "cover" }}
                        onError={(e) => { e.target.src = placeholderImage; }} // Fallback for invalid image URL
                    />
                    <h3>{item.title || "No Title"}</h3>
                    <p>{item.price || "No Price"}</p>
                    <p>{item.size || "No Size"}</p>
                    <p><strong>Platform:</strong> {item.platform || "Unknown"}</p>
                    <a
                        href={item.product_link || item.link || item.item_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                            display: "inline-block",
                            marginTop: "10px",
                            padding: "8px 12px",
                            backgroundColor: "#007BFF",
                            color: "#fff",
                            textDecoration: "none",
                            borderRadius: "4px"
                        }}
                    >
                        View on {item.platform || "Platform"}
                    </a>
                </div>
            ))}
        </div>
    );
};


export default Results;



