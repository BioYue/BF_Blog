import uuid

def generate_trace_code():
    return str(uuid.uuid4()).replace('-', '')[:12]

if __name__ == '__main__':
    print(generate_trace_code())