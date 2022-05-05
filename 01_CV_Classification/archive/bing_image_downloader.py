# Bing download
import bing_image_downloader 

query_string = 'lewis grabban'
output_dir = 'images'
bing_image_downloader.download(query_string, limit=100,  output_dir=output_dir, 
                    adult_filter_off=True, force_replace=False, 
                    timeout=60, verbose=True)