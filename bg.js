chrome.action.onClicked.addListener(async (tab) => {
  if (!tab?.id) return;

  try {
    await chrome.scripting.executeScript({
      target: { tabId: tab.id, allFrames: true },
      files: ["content.js"]
    });
  } catch (e) {
    console.warn("Kendo Evidence Helper: failed to inject content.js", e);
  }
});