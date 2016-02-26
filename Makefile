NAME=gnt-storage-eql
BUILD_SUFFIX    :=$(shell if [ -n "$(BUILD_NUMBER)" ]; then echo "-build$(BUILD_NUMBER)"; else echo ""; fi)
VERSION         :=$(shell git describe --tags --always|sed 's/^v//g')$(BUILD_SUFFIX)
DIR=$(NAME)-$(VERSION)

PREFIX=/

.PHONY: default
default: deb
package: deb

.PHONY: clean
clean:
	rm -fr $(NAME)-* || true
	rm -f *.deb
	rm -f *.rpm

$(DIR):
	mkdir "$(DIR)"
	mkdir -p "$(DIR)/usr/share/ganeti/extstorage/eql/common"
	mkdir -p "$(DIR)/etc/ganeti/extstorage"
	cp -r common/*.py "$(DIR)/usr/share/ganeti/extstorage/eql/common"
	cp eql.conf "$(DIR)/etc/ganeti/extstorage/eql.conf"
	cp attach "$(DIR)/usr/share/ganeti/extstorage/eql/"
	cp create "$(DIR)/usr/share/ganeti/extstorage/eql/"
	cp detach "$(DIR)/usr/share/ganeti/extstorage/eql/"
	cp grow "$(DIR)/usr/share/ganeti/extstorage/eql/"
	cp remove "$(DIR)/usr/share/ganeti/extstorage/eql/"
	cp setinfo "$(DIR)/usr/share/ganeti/extstorage/eql/"
	cp verify "$(DIR)/usr/share/ganeti/extstorage/eql/"
	cp parameters.list "$(DIR)/usr/share/ganeti/extstorage/eql/"

.PHONY: deb
deb: $(DIR)
	fpm -s dir -t deb -v $(VERSION) -n $(NAME) \
		-d "ganeti (>= 2.10.0)" \
		-d "python-paramiko" \
		-a all --prefix $(PREFIX) -C $(DIR) .

.PHONY: rpm
rpm: $(DIR)
	fpm -s dir -t rpm -v $(VERSION) -n $(NAME) \
		-d "ganeti >= 2.10.0" \
		-d "python-paramiko" \
		-a all --prefix $(PREFIX) -C $(DIR) .

