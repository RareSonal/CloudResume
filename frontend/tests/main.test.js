/**
 * @jest-environment jsdom
 */

import { fetchVisitorCount, downloadResume } from '../main.js';

describe('Frontend Testing', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    document.body.innerHTML = ''; // Reset DOM
  });

  test('should fetch visitor count and update the counter element', async () => {
    // Mock fetch response
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ count: 42 }),
      })
    );

    // Setup DOM
    document.body.innerHTML = '<div id="counter"></div>';

    await fetchVisitorCount();

    expect(document.getElementById('counter').textContent).toBe('42');
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/api/visitor'));
  });

  test('should handle errors when fetching visitor count', async () => {
    global.fetch = jest.fn(() => Promise.reject(new Error('Network error')));
    console.error = jest.fn(); // Mock console.error

    await fetchVisitorCount();

    expect(console.error).toHaveBeenCalledWith(
      'Error fetching visitor count:',
      expect.any(Error)
    );
  });

  test('should download resume file', async () => {
    const blob = new Blob(['dummy resume content'], { type: 'application/pdf' });

    // Mock fetch for resume
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        blob: () => Promise.resolve(blob),
      })
    );

    // Mock createObjectURL & revokeObjectURL
    const fakeUrl = 'blob:http://localhost/fake-url';
    const createObjectURLMock = jest.fn(() => fakeUrl);
    const revokeObjectURLMock = jest.fn();
    global.URL.createObjectURL = createObjectURLMock;
    global.URL.revokeObjectURL = revokeObjectURLMock;

    // Mock a element and its click method
    const clickMock = jest.fn();
    document.createElement = jest.fn(() => ({
      href: '',
      download: '',
      click: clickMock,
    }));

    await downloadResume();

    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/api/resume'));
    expect(createObjectURLMock).toHaveBeenCalledWith(blob);
    expect(clickMock).toHaveBeenCalled();
    expect(revokeObjectURLMock).toHaveBeenCalledWith(fakeUrl);
  });
});
