"""ArtifactManager - Build artifacts storage

IntentHash¹¹: 0x2D5A8F7C_P3_1_FORGE_COMPLETE_20260303T0318Z

Manages build artifacts and caching.
"""

import json
import os
from typing import Dict, Any, List, Tuple
import time


class ArtifactManager:
    """Manage build artifacts"""
    
    def __init__(self, artifacts_dir: str = "artifacts"):
        self.artifacts_dir = artifacts_dir
        self.artifacts = {}
        self._load_artifacts()
    
    def _load_artifacts(self):
        """Load artifacts registry"""
        registry_path = os.path.join(self.artifacts_dir, "artifacts.json")
        
        if os.path.exists(registry_path):
            with open(registry_path, 'r') as f:
                data = json.load(f)
                self.artifacts = data.get('artifacts', {})
    
    def store_artifact(
        self,
        artifact_name: str,
        artifact_path: str,
        metadata: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Store build artifact
        
        Args:
            artifact_name: Artifact name
            artifact_path: Path to artifact
            metadata: Artifact metadata
        
        Returns:
            Tuple of (status: SUCCESS/FAILED, artifact_id)
        """
        try:
            artifact_id = f"artifact_{int(time.time())}"
            
            self.artifacts[artifact_id] = {
                'artifact_id': artifact_id,
                'artifact_name': artifact_name,
                'artifact_path': artifact_path,
                'metadata': metadata,
                'created_at': time.time()
            }
            
            self._save_artifacts()
            
            return 'SUCCESS', artifact_id
        
        except Exception as e:
            return 'FAILED', ''
    
    def get_artifact(
        self,
        artifact_id: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Get artifact by ID
        
        Args:
            artifact_id: Artifact identifier
        
        Returns:
            Tuple of (status: SUCCESS/FAILED, artifact)
        """
        artifact = self.artifacts.get(artifact_id)
        
        if artifact:
            return 'SUCCESS', artifact
        else:
            return 'FAILED', {}
    
    def list_artifacts(
        self,
        artifact_name: str = None
    ) -> List[Dict[str, Any]]:
        """List artifacts
        
        Args:
            artifact_name: Filter by artifact name
        
        Returns:
            List of artifacts
        """
        artifacts = list(self.artifacts.values())
        
        if artifact_name:
            artifacts = [a for a in artifacts if a['artifact_name'] == artifact_name]
        
        return artifacts
    
    def _save_artifacts(self):
        """Save artifacts registry"""
        os.makedirs(self.artifacts_dir, exist_ok=True)
        registry_path = os.path.join(self.artifacts_dir, "artifacts.json")
        
        with open(registry_path, 'w') as f:
            json.dump({'artifacts': self.artifacts}, f, indent=2)
