import os
import whois
import requests

class Wisdom:
    def __init__(self):
        self.all_chars_permutations = []
        self.all_words_permutations = []
        self.words = []
        self.words = self.readwords()
        self.domains = []
        self.outfile = open('freedomains.txt','w')

    def readwords(self):
        with open('keywords.txt','r') as f:
            for line in f.readlines():
                line = line.strip()
                self.words.append(line)
        return self.words

    def run(self):
        print self.words

    def cut_end(self, word):
        word_variants = []
        for i in range(1, len(word)):
            word_variants.append(word[0:i])
        return word_variants

    def cut_beg(self, word):
        word_variants = []
        for i in range(0, (len(word)-1)):
            word_variants.append(word[i:len(word)])
        return word_variants

    def generate_char_permutations(self):
        for word in self.words:
            for i in self.cut_beg(word):
                self.all_chars_permutations.append(i)
            for i in self.cut_end(word):
                self.all_chars_permutations.append(i)
        print self.all_chars_permutations
        return self.all_chars_permutations

    def generate_all_permutations(self):
        for chunk1 in range(0,len(self.all_chars_permutations)):
            for chunk2 in range(0,len(self.all_chars_permutations)):
                if chunk2 != chunk1:
                    domain = self.all_chars_permutations[chunk1] + self.all_chars_permutations[chunk2] + '.com'
                    self.domains.append(domain)
        return self.domains
    
    def check_twitter_handle(self, domain):
        r = requests.get("http://twitter.com/" + domain.strip('.com'))
        if r.status_code == 200:
            return ':t'
        else:
            return ''

    def generate_domains(self):
        i = 0
        for domain in self.domains:
            i = i + 1
            print "checking domain %s %i/%i" % (domain, i, len(self.domains))
            try:
                w = whois.whois(domain)
            except whois.parser.PywhoisError:
                print 'Domain %s is not registered' % domain
                twitter_flag = self.check_twitter_handle(domain)
                self.outfile.write(domain + ' ' + twitter_flag + '\n')

w = Wisdom()
w.generate_char_permutations()
w.generate_all_permutations()
w.generate_domains()
