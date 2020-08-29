from src.dds import DDS

def hello(request):
    # return "Hello awX!"

    # Default for maximum threads is to let the library decide
    mt = 0
    # Default for maximum memory is to let the library decide
    mm = 0

    dds = DDS(max_threads=mt, max_memory=mm)    
    data = request.get_json(silent=True)
    dds_table = dds.calc_dd_table(data['hands'])
    return dds_table
