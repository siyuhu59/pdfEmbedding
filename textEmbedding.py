from FlagEmbedding import BGEM3FlagModel

class EmbeddingGenerator:
    def __init__(self, model_name='BAAI/bge-m3'):
        """모델을 초기화합니다."""
        self.model = BGEM3FlagModel(model_name, use_fp16=True)
    
    def generate_embeddings(self, texts):
        """
        텍스트를 임베딩 벡터로 변환합니다.
        
        Args:
            texts (list of str): 임베딩할 문장 또는 텍스트의 리스트
        
        Returns:
            dict: Dense 벡터 값이 담긴 딕셔너리
        """
        embeddings = self.model.encode(texts, return_dense=True)
        return embeddings['dense_vecs']


if __name__ == "__main__":
    # 임베딩 생성기 객체 생성
    embedding_generator = EmbeddingGenerator()

    # 예시 문장
    texts = ["이 조항은 개정되었습니다.", "이것은 신설된 조항입니다."]

    # 임베딩 생성
    embeddings = embedding_generator.generate_embeddings(texts)
    
    print(embeddings)
