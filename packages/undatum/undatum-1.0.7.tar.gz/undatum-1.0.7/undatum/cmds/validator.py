from xlrd import open_workbook
from operator import itemgetter, attrgetter
import csv
import zipfile
import sys
import json
import bson
import logging
#from xmlr import xmliter
import xml.etree.ElementTree as etree
from collections import defaultdict
from ..utils import get_file_type, get_option, write_items, get_dict_value, strip_dict_fields, dict_generator
import dictquery as dq
from ..validate import VALIDATION_RULEMAP


class Validator:
    def __init__(self):
        pass

    def validate(self, fromfile, options={}):
        """Validates selected field against validation rule"""
        logging.debug('Processing %s' % fromfile)
        f_type = get_file_type(fromfile) if options['format_in'] is None else options['format_in']
        if options['zipfile']:
            z = zipfile.ZipFile(fromfile, mode='r')
            fnames = z.namelist()
            if f_type == 'bson':
                infile = z.open(fnames[0], 'rb')
            else:
                infile = z.open(fnames[0], 'r')
        else:
            if f_type == 'bson':
                infile = open(fromfile, 'rb')
            else:
                infile = open(fromfile, 'r', encoding=get_option(options, 'encoding'))
        to_file = get_option(options, 'output')
        if to_file:
            to_type = get_file_type(to_file)
            if not to_file:
                logging.debug('Output file type not supported')
                return
            out = open(to_file, 'w', encoding='utf8')
        else:
            to_type = 'csv'
            out = sys.stdout
        fields = options['fields'].split(',')
        val_func = VALIDATION_RULEMAP[options['rule']]
        logging.info('uniq: looking for fields: %s' % (options['fields']))
        validated = []
        stats = {'total': 0, 'invalid': 0, 'novalue' : 0}
        if f_type == 'csv':
            delimiter = get_option(options, 'delimiter')
            reader = csv.DictReader(infile, delimiter=delimiter)
            n = 0
            for r in reader:
                n += 1
                if n % 1000 == 0:
                    logging.info('uniq: processing %d records of %s' % (n, fromfile))
                if options['filter'] is not None:
                    if not dq.match(r, options['filter']):
                        continue
                res = val_func(r[fields[0]])
                stats['total'] += 1
                if not res:
                    stats['invalid'] += 1
                validated.append({fields[0] : r[fields[0]], fields[0] + '_valid' : res})

        elif f_type == 'jsonl':
            n = 0
            for l in infile:
                n += 1
                if n % 10000 == 0:
                    logging.info('uniq: processing %d records of %s' % (n, fromfile))
                r = json.loads(l)
                if options['filter'] is not None:
                    if not dq.match(r, options['filter']):
                        continue
                stats['total'] += 1
                values = get_dict_value(r, fields[0].split('.'))
                if len(values) > 0:
                    res = val_func(values[0])
                    if not res:
                        stats['invalid'] += 1
                    validated.append({fields[0] : values[0], fields[0] + '_valid' : res})
                else:
                    stats['novalue'] += 1

        elif f_type == 'bson':
            uniqval = []
            bson_iter = bson.decode_file_iter(infile)
            n = 0
            for r in bson_iter:
                n += 1
                if n % 1000 == 0:
                    logging.info('uniq: processing %d records of %s' % (n, fromfile))
                if options['filter'] is not None:
                    if not dq.match(r, options['filter']):
                        continue
                stats['total'] += 1
                values = get_dict_value(r, fields[0].split('.'))
                if len(values) > 0:
                    res = val_func(values[0])
                    if not res:
                        stats['invalid'] += 1
                    validated.append({fields[0] : values[0], fields[0] + '_valid' : res})
                else:
                    stats['novalue'] += 1
        else:
            logging.error('Invalid filed format provided')
            return
        infile.close()
        stats['share'] = 100.0 * stats['invalid'] / stats['total']
        logging.debug('validate: complete, %d records (%.2f%%) not valid and %d (%.2f%%) not found of %d against %s' % (stats['invalid'], stats['share'], stats['novalue'], 100.0 * stats['novalue'] / stats['total'], stats['total'], options['rule']))
        if options['mode'] != 'stats':
            writer = csv.DictWriter(out, fieldnames=[fields[0], fields[0] + '_valid'], delimiter=get_option(options, 'delimiter'))
            for row in validated:
                if options['mode'] == 'invalid':
                    if not row[fields[0] + '_valid']:
                        writer.writerow(row)
                elif options['mode'] == 'all':
                    writer.writerow(row)
        else:
            out.write(json.dumps(stats, indent=4))

