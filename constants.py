method_value_table = "mv_analysis"
time_value_fee_table = "tvf_analysis"
tables = [
    {"table":time_value_fee_table, "columns":["Time", "total_value", "total_txn_fee"]}, 
    {"table":method_value_table, "columns":["Method" ,"sum_val" ]},]
socket_port = 3000
