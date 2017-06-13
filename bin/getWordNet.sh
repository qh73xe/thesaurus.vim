# このスクリプトは英語 Word net のデータベースをダウンロードします.
THISDIR=$(dirname "${0}")
DATADIR=$(readlink -f "${THISDIR}/../var")
URL="http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz"

# DB ファイルの取得
wget "${URL}"
gzip -d "wnjpn.db.gz"

# DB ファイルのデプロイ
mv wnjpn.db "${DATADIR}"
