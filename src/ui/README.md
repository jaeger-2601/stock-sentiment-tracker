# Stock Sentiment Tracker UI

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

### Setup
The frontend used to use create-react-app but it has been ejected. To install all dependencies, run:
```bash
npm install
```

### Execution


##### Data Representation
1. Ensure InfluxDB is running
2. Ensure Backend API is running
3. Run Frontend
```bash
npm start
```
To create optimized production build, run:
```bash
npm run build
```
To server production build, run:
```bash
npm install -g serve
serve -s build
```