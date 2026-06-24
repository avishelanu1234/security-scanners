// Enhanced retry logic with exponential backoff and jitter
public void enhancedRetryLogic() {
    int maxRetries = 5;
    int retryCount = 0;
    while (retryCount < maxRetries) {
        try {
            // Attempt the operation
            performOperation();
            break; // Exit loop on success
        } catch (Exception e) {
            retryCount++;
            long waitTime = (long) (Math.pow(2, retryCount) * 1000 + Math.random() * 1000);
            Thread.sleep(waitTime);
        }
    }
}