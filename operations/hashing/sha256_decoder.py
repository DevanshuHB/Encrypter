# SHA256 is a hash function and cannot be decoded. This class will provide a method to verify if a given input matches a given SHA256 hash.

import hashlib

class SHA256Decoder:
    def execute(self, input_data):
        # Expect input_data as "text||hash" to verify
        try:
            text, hash_to_compare = input_data.split('||')
        except ValueError:
            return "Input format error. Use 'text||hash' format."
        sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if sha256_hash == hash_to_compare:
            return "Verification successful: Hash matches."
        else:
            return "Verification failed: Hash does not match."
