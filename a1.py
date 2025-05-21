/* Make the entire chat container wider */

html, body {
    width: 100%;
    margin: 0;
    padding: 0;
}

.chainlit-app {
    width: 100vw;
}

/* Optional: Stretch the message bubbles */
.message-bubble {
    max-width: 100% !important;
}

table th {
    padding: 4px 8px !important;
    border: 1px solid #cccccc !important;
    background-color: #dcdcdc;
    color: #1a1a1a !important;
}

table tr {
    height: 60px !important;;
}

table td {
    padding: 4px 8px !important;
    vertical-align: top !important;
    border: 1px solid #cccccc !important;
}

/* Lighter hover color */
table tr:hover {
    background-color: #fafafa;  /* light gray on hover */
}

table td,
table th {
    min-width: 200px;
    max-width: 200px;
    overflow-wrap: break-word; /* Allows long words to break and wrap onto the next line */
    white-space: normal;        /* Enables normal text wrapping behavior */
}

table {
    margin: 10px;
}
