"""Test script to verify IP recognizer handles both IPv4 and IPv6."""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer.predefined_recognizers.generic.ip_recognizer import IpRecognizer

def test_ip_recognizer():
    """Test the IP recognizer with IPv4 and IPv6 addresses."""
    
    recognizer = IpRecognizer()
    
    test_cases = [
        # IPv4 tests
        ("Server IP: 192.168.1.1", "IPv4: 192.168.1.1"),
        ("Connect to 10.0.0.1", "IPv4: 10.0.0.1"),
        ("Public IP 8.8.8.8", "IPv4: 8.8.8.8"),
        
        # IPv6 tests
        ("IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334", "IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334"),
        ("Short IPv6: 2001:db8::1", "IPv6: 2001:db8::1"),
        ("Localhost IPv6: ::1", "IPv6: ::1"),
        ("IPv6: fe80::1", "IPv6: fe80::1"),
        ("Full IPv6: 2001:0db8:0000:0000:0000:0000:0000:0001", "IPv6: 2001:0db8:0000:0000:0000:0000:0000:0001"),
        
        # Mixed
        ("IPv4: 192.168.1.1 and IPv6: 2001:db8::1", "Both"),
        
        # Invalid
        ("Invalid: 999.999.999.999", "None (invalid IPv4)"),
        ("Not an IP: 192.168.1", "None (incomplete)"),
    ]
    
    print("=" * 70)
    print("IP ADDRESS RECOGNIZER TEST (IPv4 & IPv6)")
    print("=" * 70)
    
    for text, expected in test_cases:
        results = recognizer.analyze(text, ["IP_ADDRESS"])
        
        print(f"\nText: '{text}'")
        print(f"Expected: {expected}")
        
        if results:
            detected = []
            for result in results:
                ip_addr = text[result.start:result.end]
                detected.append(f"{ip_addr} (score: {result.score:.2f})")
            print(f"Detected: {', '.join(detected)}")
        else:
            print("Detected: None")
        
        print("-" * 70)
    
    print("\n✅ IP Address Recognizer test completed!")

if __name__ == "__main__":
    test_ip_recognizer()
